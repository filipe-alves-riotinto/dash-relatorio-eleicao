import pandas as pd
from .fichas import fichas 
from .fefc import fefc
from .votos import votacao
from .municipio import municipio
from .eleitorado import eleitorado


def base_federal(ano):
    df_temp_municipio = municipio()[['uf_cand', 'no_regiao_brasil', 'id_uf', 'co_regiao_brasil']].drop_duplicates().reset_index(drop=True)
    df_eleitorado = (eleitorado(ano)[['SG_UF', 'QT_ELEITORES_PERFIL']]
                    .groupby('SG_UF', as_index=False)['QT_ELEITORES_PERFIL']
                    .sum()
                    .rename(columns={'SG_UF': 'uf_cand', 'QT_ELEITORES_PERFIL': 'Eleitorado'}))

    df_resultado = pd.merge(
    pd.merge(
        pd.merge(
            pd.merge(
            #UNIR FICHA COM MUNICIPIO
            fichas(ano),
            df_temp_municipio,
            left_on='uf_cand',
            right_on='uf_cand',
            how='left'
            ),
                #UNIR COM ELEITORADO
                df_eleitorado,
                on='uf_cand',
                how='left'
                ),
                    #UNIR COM FEFC
                    fefc(ano),
                    left_on=['id_cand', 'nm_partido'],
                    right_on=['id_cand', 'nm_doador'],
                    how='left'
                    ),
                        #UNIR COM VOTOS
                    votacao(ano),
                    on='id_cand',
                    how='left',
                    )
    return df_resultado


def base_estadual(ano):
    df_eleitorado = eleitorado(ano).groupby(['SG_UF', 'CD_MUNICIPIO'])['QT_ELEITORES_PERFIL'].sum().reset_index()
    df_eleitorado = df_eleitorado.rename(columns={
        'SG_UF': 'sg_uf',
        'CD_MUNICIPIO': 'id_municipio',
        'QT_ELEITORES_PERFIL': 'Eleitorado'
    })
    #print(df_eleitorado)
    df_resultado = pd.merge(
    pd.merge(
        pd.merge(
            pd.merge(
            #UNIR FICHA COM MUNICIPIO
            fichas(ano),
            municipio().drop(['uf_cand','nm_municipio'], axis=1),
            on='id_municipio',
            how='left'
            ),
                #UNIR COM ELEITORADO
                df_eleitorado,
                on='id_municipio',
                how='left'
                ),
                    #UNIR COM FEFC
                    fefc(ano),
                    left_on=['id_cand', 'nm_partido'],
                    right_on=['id_cand', 'nm_doador'],
                    how='left'
                    ),
                        #UNIR COM VOTOS
                    votacao(ano).drop(['id_municipio'], axis=1),
                    on='id_cand',
                    how='left',
                    )
    return df_resultado


# print(base_federal('2022').dtypes)
# print(base_federal('2022'))
#print("Colunas do primeiro DataFrame:", base_federal('2022').columns.tolist())
#print(base_federal('2022'))
#base_estadual('2024').to_excel('/mnt/e/PSDB/RelatorioFEFCtse2024V1.xlsx', index=False)