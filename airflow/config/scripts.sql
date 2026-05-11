create database concolit_db;

create table if not exists periodos (
    id uuid primary key default gen_random_uuid(),
    fecha_inicial date not null,
    fecha_final date not null,
    saldo_inicial NUMERIC(18,2) not null,
    saldo_final NUMERIC(18,2) not null,
    constraint ck_pe_fechas check ( fecha_inicial <= fecha_final )
);

create table if not exists mayor (
    id uuid primary key default gen_random_uuid(),
    id_periodo uuid not null,
    sociedad varchar(32),
    cuenta varchar(32),
    asignacion varchar(64),
    documento varchar(32),
    ejercicio_mes date,
    clase_doc varchar(32),
    fecha_doc date,
    fecha_contabilizacion date,
    clave_contabilizacion varchar(32),
    importe_moneda_doc NUMERIC(18,2),
    moneda_doc varchar(16),
    importe_moneda_local NUMERIC(18,2),
    moneda_local varchar(16),
    texto_cab_doc varchar(512),
    texto varchar(512),
    cuenta_contrapartida varchar(32),
    referencia varchar(512),
    importe_valorado_ml2 NUMERIC(18,2),
    constraint fk_ma_pe foreign key (id_periodo) references periodos (id)
);

create index if not exists index_mayor_asignacion on mayor(asignacion);

create table if not exists tildes_periodo (
    id uuid primary key default gen_random_uuid(),
    id_mayor uuid not null,
    tilde varchar(16) not null,
    fecha timestamptz not null default now(),
    constraint ck_ti_tilde check ( tilde in ('A', 'B', 'C') )
);

create or replace function fn_mayor_to_classify (par_id_periodo uuid)
returns table (
    id_mayor uuid,
    id_periodo uuid,
    asignacion varchar(64),
    importe_valorado_ml2 NUMERIC(18,2)
              )
as $$
    begin
        return query
        select
            m.id,
            m.id_periodo,
            m.asignacion,
            m.importe_valorado_ml2
        from mayor m
        where m.id_periodo = par_id_periodo;
end;
$$ language plpgsql;

alter table tildes_periodo add constraint fk_ti_ma foreign key (id_mayor) references mayor (id);

alter table tildes add column id_periodo uuid not null;

alter table tildes add constraint fk_ti_pe foreign key (id_periodo) references periodos (id);

create table empresas (
    id uuid primary key not null default gen_random_uuid(),
    razon_social varchar(64) not null,
    cuit numeric(11, 0)
);

create table cuentas (
    id uuid primary key not null default gen_random_uuid(),
    descripcion varchar(64),
    comentario varchar(256),
    id_empresa uuid not null,
    constraint fk_cu_em foreign key (id_empresa) references empresas (id)
);

alter table periodos add column id_cuenta uuid not null;

alter table periodos add constraint fk_pe_cu foreign key (id_cuenta) references cuentas (id);

alter table periodos rename column fecha_final to fecha;
alter table periodos drop column fecha_inicial;

alter table periodos rename column saldo_final to saldo_usd;
alter table periodos rename column saldo_inicial to saldo_ars;

alter table tildes rename to estado_partidas;

alter table estado_partidas rename column tilde to cerrado;

alter table estado_partidas drop constraint ck_ti_tilde;

alter table estado_partidas
    alter column cerrado type boolean
    using cerrado::boolean
;

create table asociaciones (
    id uuid primary key not null default gen_random_uuid(),
    id_partida_positiva uuid not null unique,
    id_partida_negativa uuid not null unique,
    constraint fk_aso_pos_mayor foreign key (id_partida_positiva) references mayor (id),
    constraint fk_aso_neg_mayor foreign key (id_partida_negativa) references mayor (id),
    constraint un_aso unique (id_partida_positiva, id_partida_negativa)
);

drop table estado_partidas;

alter table mayor add column anterior boolean default False;

alter table mayor add column id_cuenta uuid;
alter table mayor add constraint fk_may_cue foreign key (id_cuenta) references cuentas (id);

alter table mayor drop column id_periodo;

create function fn_asignaciones_pendientes(par_id_cuenta uuid, par_fecha_corte date) returns TABLE(id_cuenta uuid, asignacion character varying, subtotal numeric)
	language plpgsql
as $$
        begin
            return query
            select
                m.id_cuenta,
                m.asignacion,
                sum(m.importe_valorado_ml2) as subtotal
            from mayor m
            inner join cuentas c
            on m.id_cuenta = c.id
            where
                c.id = par_id_cuenta
                and fecha_contabilizacion <= par_fecha_corte
                and anterior != True
            group by m.id_cuenta, m.asignacion
            having sum(m.importe_valorado_ml2) > 0;
        end;
    $$;

create or replace function fn_previo_partidas_pendientes
    (par_id_cuenta uuid, par_fecha_corte date)
    returns table (
        id uuid,
        sociedad varchar(32),
        cuenta varchar(32),
        asignacion varchar(64),
        documento varchar(32),
        ejercicio_mes date,
        clase_doc varchar(32),
        fecha_doc date,
        fecha_contabilizacion date,
        clave_contabilizacion varchar(32),
        importe_moneda_doc numeric(18, 2),
        moneda_doc varchar(16),
        importe_moneda_local numeric(18, 2),
        moneda_local varchar(16),
        texto_cab_doc varchar(512),
        texto varchar(512),
        cuenta_contrapartida varchar(32),
        referencia varchar(512),
        importe_valorado_ml2 numeric(18, 2),
        anterior boolean,
        id_cuenta uuid
    )
    language plpgsql
    as $$
        begin
            return query
            with cte_mayor_partidas_agrupadas_historico as ( -- REGISTRAMOS ASIGNACIONES CON SUBTOTAL > 0 DEL TOTAL MESES
                select *
                from fn_asignaciones_pendientes(par_id_cuenta, par_fecha_corte)
            )
            -- OBTENEMOS TODAS LAS PARTIDAS QUE COINCIDEN EL IMPORTE CON EL SUBTOTAL POSITIVO
            select
            m.*
            from cte_mayor_partidas_agrupadas_historico as cte
            inner join mayor m
            on cte.asignacion = m.asignacion
            and m.importe_valorado_ml2 > 0
            and m.importe_valorado_ml2 = cte.subtotal
            inner join cuentas c
                on m.id_cuenta = c.id
                and c.id = par_id_cuenta
            where m.fecha_contabilizacion <= par_fecha_corte
            ;
        end;
    $$;

create function fn_analizar_via_pandas(par_id_cuenta uuid, par_fecha_corte date) returns TABLE(id uuid, sociedad character varying, cuenta character varying, asignacion character varying, documento character varying, ejercicio_mes date, clase_doc character varying, fecha_doc date, fecha_contabilizacion date, clave_contabilizacion character varying, importe_moneda_doc numeric, moneda_doc character varying, importe_moneda_local numeric, moneda_local character varying, texto_cab_doc character varying, texto character varying, cuenta_contrapartida character varying, referencia character varying, importe_valorado_ml2 numeric, anterior boolean, id_cuenta uuid)
	language plpgsql
as $$
    begin
        return query
            with cte_asignaciones_para_pandas as (
                select fn_ppp.asignacion
                from fn_asignaciones_pendientes(
                     par_id_cuenta,
                     par_fecha_corte
                     ) fn_ppp
                left join fn_previo_partidas_pendientes(
                          par_id_cuenta,
                        par_fecha_corte
                          ) fn_ap
                on fn_ap.asignacion = fn_ppp.asignacion
                where fn_ap.asignacion is null
            )
        select m.*
        from mayor m
        inner join cte_asignaciones_para_pandas
        on m.asignacion = cte_asignaciones_para_pandas.asignacion
        where m.id_cuenta = par_id_cuenta
        and m.fecha_contabilizacion <= par_fecha_corte;
    end;
$$;
