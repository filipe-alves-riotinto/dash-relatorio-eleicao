import pandas as pd
from .fichas import fichas 
from .fefc import fefc
from .votos import votacao
from .municipio import municipio
from .eleitorado import eleitorado

def fichas_processada(ano):
    df = pd.merge(
        fichas(ano),
        municipio(),
        left_on='munCandidatura',
        right_on='id_municipio',
        how='left'
    )

    return df

#print(fichas_processada(2024))
def base_federal1(ano, tipo=None):
    df_votos = votacao(ano, tipo)
    df_resultado = pd.merge(
            pd.merge(
        pd.merge(
            df_votos,
            fichas(ano).drop('nm_municipio', axis=1),
            on='id_cand',
            how='inner'
        ),
        fefc(ano),
        on='id_cand',
        how='left',
        ),
        municipio(),
        on='id_municipio',
        #right_on=['uf_cand', 'nm_municipio'],
        how='left'
    )
    return df_resultado

def base_federalbk(ano, tipo=None):
    df_votos = votacao(ano, tipo)
    # SOMA  DE TODOS OS VOTOS BR
    if tipo == 'federal':
        df_municipio = municipio()
        df_municipio = df_municipio.groupby(['uf_cand', 'id_uf']).agg({
            'nu_pop': 'sum'
        }).reset_index()
        
        df_eleitorado = eleitorado()[['id_uf','Eleitorado']]
        df_eleitorado = df_eleitorado.groupby('id_uf').sum('Eleitorado')
 
        #unir com votos
        df_resultado = pd.merge(
                    pd.merge(
                pd.merge(
            pd.merge(
                fichas(ano),
                df_votos,
                on='id_cand',
                how='left'
            ),
        #unir FEFC
            fefc(ano),
            on='id_cand',
            how='left',
        ),
        #unir Municipio
        df_municipio,
        on='uf_cand',
        how='left'
        ),
        #unir Eleitorado
        df_eleitorado,
        on='id_uf',
        how='left'
    )
    #SOMA DE VOTOS POR ESTADO    
    elif tipo == 'estadual':
        
        pass
    #VOTOS POR MUNICIPIO
    elif tipo =='municipal':
        
        pass
    
    return df_resultado

def base_federal(ano):
    df_temp_municipio = municipio()[['uf_cand', 'no_regiao_brasil', 'id_uf', 'co_regiao_brasil']].drop_duplicates().reset_index(drop=True)
    
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
                eleitorado('2022').rename(columns={'UF':'uf_cand'}),
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
                    votacao(ano, tipo='federal'),
                    on='id_cand',
                    how='left',
                    )
    return df_resultado


def base_estadual(ano):
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
                eleitorado(ano).drop(['id_uf'], axis=1),
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
#base_federal(2022, tipo='federal')