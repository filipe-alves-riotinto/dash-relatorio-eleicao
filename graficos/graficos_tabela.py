import streamlit as st

def grafico_tabela_dados(base):
    base = base.copy()
    base['valor por voto'] = (base['FEFC'] / base['qt_votos_nom_validos']).replace(0, 1).round(2)
    colunas = ['uf_cand','nm_municipio', 'nm_cand', 'sg_partido', 'ds_eleicao', 'nm_cargo', 'ds_raca', 'ds_genero','FEFC','qt_votos_nom_validos', 'valor por voto', 'Eleitorado']
    #base = base[base['nm_cargo'] == filtro]
    base = base.sort_values("qt_votos_nom_validos", ascending=False)
    st.dataframe (base[colunas],
                  column_config={
                        'uf_cand': st.column_config.TextColumn("UF"),
                        'nm_municipio': st.column_config.TextColumn("Municipio"),
                        'nm_cand': st.column_config.TextColumn("Nome do Candidato"),
                        'sg_partido': st.column_config.TextColumn("Partido"),
                        'ds_eleicao': st.column_config.TextColumn("Resultado"),
                        'nm_cargo': st.column_config.TextColumn("Cargo"),
                        'ds_raca': st.column_config.TextColumn("Raça"),
                        'ds_genero': st.column_config.TextColumn("Genero"),
                        #'li_foto': st.column_config.ImageColumn("Foto", help="Foto do candidato"),
                        "qt_votos_nom_validos": st.column_config.NumberColumn("Votos", format="localized" ),
                        "Eleitorado": st.column_config.NumberColumn("Eleitorado", format="localized" ),
                        #'nm_doador': st.column_config.TextColumn("Nome Doador"),
                        'FEFC': st.column_config.NumberColumn("FFEC", format="dollar", help="Valor de recursos FEFC"),
                        'valor por voto': st.column_config.NumberColumn("Valor por voto", format="dollar", help="Valor de recursos FEFC"),
                  }, hide_index=True)