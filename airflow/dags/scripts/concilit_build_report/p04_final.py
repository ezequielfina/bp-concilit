import os

from ..utils.engine_db import get_hook_sql
import pandas as pd
from pandas import ExcelWriter

from airflow.decorators import task

from ..p_update_status import (
    update_status_reporte_saldo_bancario,
    update_extension_reporte_saldo_bancario
)

RESULTS_PATH = '/data/results/'


@task
def final_report(prev_info: dict):

    id_saldo_bancario: str = prev_info['id_saldo_bancario']

    try:

        update_status_reporte_saldo_bancario(
            id_saldo_bancario,
            'Calculando valores finales'
        )

        csv_path = os.path.join(
            RESULTS_PATH,
            f'{id_saldo_bancario}.csv'
        )

        df = pd.read_csv(csv_path)

        subtotal_ars = df['importe_valorado_ml2'].sum()
        subtotal_usd = df['importe_moneda_local'].sum()

        hook_sql = get_hook_sql()

        records = hook_sql.get_records(
            'SELECT * FROM fn_saldo_bancario(%(id)s)',
            parameters={'id': id_saldo_bancario}
        )

        excel_path = os.path.join(
            RESULTS_PATH,
            f'{id_saldo_bancario}.xlsx'
        )

        with ExcelWriter(excel_path, engine='xlsxwriter') as writer:  # noqa # type: ignore

            workbook = writer.book

            # =========================================================
            # FORMATOS
            # =========================================================

            formats = {

                'title': workbook.add_format({
                    'bold': True,
                    'font_size': 11
                }),

                'subtitle': workbook.add_format({
                    'bold': True,
                    'underline': 1
                }),

                'table_header': workbook.add_format({
                    'bold': True,
                    'bg_color': '#FFFFCC',
                    'border': 1,
                    'align': 'center'
                }),

                'table_cell': workbook.add_format({
                    'border': 1
                }),

                'currency_ars': workbook.add_format({
                    'num_format': '$#,##0.00',
                    'border': 1
                }),

                'currency_usd': workbook.add_format({
                    'num_format': '$#,##0.00',
                    'border': 1
                }),

                'date': workbook.add_format({
                    'num_format': 'dd/mm/yyyy'
                }),

                'difference': workbook.add_format({
                    'num_format': '$ #,##0.00',
                    'border': 1,
                    'bold': True,
                    'bg_color': '#F2F2F2'
                })

            }

            # =========================================================
            # SHEET RESUMEN
            # =========================================================

            worksheet_hl = workbook.add_worksheet('0. Hoja Llave')

            worksheet_hl.hide_gridlines(2)

            worksheet_hl.set_zoom(90)

            worksheet_hl.set_column('A:A', 25)
            worksheet_hl.set_column('C:F', 20)

            if records:

                (
                    cuit,
                    razon_social,
                    cuenta,
                    descripcion_cuenta,
                    fecha,
                    saldo_ars,
                    saldo_usd
                ) = records[0]

                # =====================================================
                # TITULOS
                # =====================================================

                worksheet_hl.write(
                    'A1',
                    f'{razon_social} - {cuit}',
                    formats['title']
                )

                worksheet_hl.write(
                    'A2',
                    f'Análisis al {fecha}',
                    formats['title']
                )

                worksheet_hl.write(
                    'A4',
                    f'Conciliación de la cuenta {cuenta}',
                    formats['subtitle']
                )

                # =====================================================
                # TABLA
                # =====================================================

                headers = [
                    'Nro de Cuenta',
                    'Descripción',
                    'Importe USD',
                    'Importe ARS'
                ]

                start_row = 8
                start_col = 2

                for idx, header in enumerate(headers):

                    worksheet_hl.write(
                        start_row,
                        start_col + idx,
                        header,
                        formats['table_header']
                    )

                # =====================================================
                # DATA
                # =====================================================

                worksheet_hl.write(
                    'C10',
                    cuenta,
                    formats['table_cell']
                )

                worksheet_hl.write(
                    'D10',
                    descripcion_cuenta,
                    formats['table_cell']
                )

                worksheet_hl.write_number(
                    'E10',
                    float(saldo_usd or 0),
                    formats['currency_usd']
                )

                worksheet_hl.write_number(
                    'F10',
                    float(saldo_ars or 0),
                    formats['currency_ars']
                )

                # =====================================================
                # SUBTOTALES
                # =====================================================

                worksheet_hl.write(
                    'D13',
                    'S/ composición',
                    formats['table_cell']
                )

                worksheet_hl.write(
                    'D14',
                    'Diferencia',
                    formats['table_cell']
                )

                worksheet_hl.write_number(
                    'E13',
                    float(subtotal_usd or 0),
                    formats['currency_usd']
                )

                worksheet_hl.write_number(
                    'F13',
                    float(subtotal_ars or 0),
                    formats['currency_ars']
                )

                worksheet_hl.write_formula(
                    'E14',
                    '=E10-E13',
                    formats['currency_usd']
                )

                worksheet_hl.write_formula(
                    'F14',
                    '=F10-F13',
                    formats['difference']
                )

                # =====================================================
                # NOTAS
                # =====================================================

                worksheet_hl.write(
                    'A16',
                    'Tildes',
                    formats['subtitle']
                )

                worksheet_hl.write(
                    'A21',
                    'Notas',
                    formats['subtitle']
                )

            else:

                worksheet_hl.write(
                    'B5',
                    'Sin registro actual'
                )

            # =========================================================
            # SHEET DETALLE
            # =========================================================

            df.to_excel(
                writer,
                sheet_name='1. Partidas Pendientes CM',
                index=False
            )

            worksheet_df = writer.sheets['1. Partidas Pendientes CM']

            worksheet_df.set_zoom(90)

        update_status_reporte_saldo_bancario(
            id_saldo_bancario,
            'Construcción exitosa'
        )

        update_extension_reporte_saldo_bancario(
            id_saldo_bancario,
            '.xlsx'
        )

    except Exception as e:

        print(e)

        update_status_reporte_saldo_bancario(
            id_saldo_bancario,
            'Falló build - Construyendo el reporte final'
        )

        raise
