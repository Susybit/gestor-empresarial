import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_engine import DataEngine

def generate_full_report():
    print("Iniciando generacion de reporte analitico final...")
    
    report_dir = "reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
        
    engine = DataEngine()
    df_emp = engine.get_employees()
    df_prj = engine.get_projects()
    df_asg = engine.get_assignments()
    
    TEMPLATE = "plotly_white"
    BLUE = '#1E40AF'
    GREEN = '#10B981'
    AMBER = '#F59E0B'
    RED = '#EF4444'

    # --- 1. CAPITAL HUMANO ---
    # Antiguedad Top 5 + 5 (Veteranos y Nuevos)
    top_old = df_emp.nlargest(5, 'ANTIGUEDAD_ANOS').copy()
    top_new = df_emp.nsmallest(5, 'ANTIGUEDAD_ANOS').copy()
    top_old['Categoria'] = 'Veteranos'
    top_new['Categoria'] = 'Nuevos'
    df_ant = pd.concat([top_old, top_new])
    
    fig_ant = px.bar(df_ant, x='TX_NOMBRE', y='ANTIGUEDAD_ANOS', color='Categoria',
                    title="Ranking de Antiguedad: Top 5 Veteranos vs Nuevos", 
                    template=TEMPLATE, color_discrete_map={'Veteranos': BLUE, 'Nuevos': GREEN})
    fig_ant.write_html(f"{report_dir}/01_antiguedad_top_5_5.html")

    # Distribucion General (Boxplot de antiguedad)
    fig_box = px.box(df_emp, y="ANTIGUEDAD_ANOS", title="Distribucion General de Antiguedad (Boxplot)", template=TEMPLATE, color_discrete_sequence=[BLUE])
    fig_box.write_html(f"{report_dir}/02_antiguedad_boxplot.html")

    # Piramide de Edad con Media y Desv
    avg_age = df_emp['EDAD'].mean()
    std_age = df_emp['EDAD'].std()
    fig_age = px.histogram(df_emp, x="EDAD", title=f"Distribucion de Edad (Media: {avg_age:.1f} | Desv: {std_age:.1f})", 
                       template=TEMPLATE, color_discrete_sequence=[BLUE])
    fig_age.add_vline(x=avg_age, line_dash="dash", line_color="red")
    fig_age.write_html(f"{report_dir}/03_edades.html")

    # Estado Civil
    df_civil = df_emp.groupby('CX_EDOCIVIL').size().reset_index()
    df_civil.columns = ['Code', 'Total']
    df_civil['Estado Civil'] = df_civil['Code'].map({'S': 'Soltero/a', 'C': 'Casado/a', 'V': 'Viudo/a', 'D': 'Divorciado/a'})
    fig_civil = px.pie(df_civil, values='Total', names='Estado Civil', title="Distribucion por Estado Civil")
    fig_civil.write_html(f"{report_dir}/04_estado_civil.html")

    # --- 2. EVOLUCION TEMPORAL ---
    hires = df_emp['F_ALTA'].dt.year.value_counts().reset_index()
    hires.columns = ['Year', 'Altas']
    exits = df_emp['F_BAJA'].dt.year.value_counts().reset_index()
    exits.columns = ['Year', 'Bajas']
    evolution = pd.merge(hires, exits, on='Year', how='outer').fillna(0).sort_values('Year')
    
    # Calculo de crecimiento para el titulo
    evolution['Neto'] = evolution['Altas'] - evolution['Bajas']
    top_years = evolution.nlargest(2, 'Neto')['Year'].tolist()
    
    fig_evo = go.Figure()
    fig_evo.add_trace(go.Scatter(x=evolution['Year'], y=evolution['Altas'], name='Altas', line=dict(color=GREEN, width=4)))
    fig_evo.add_trace(go.Scatter(x=evolution['Year'], y=evolution['Bajas'], name='Bajas', line=dict(color=RED, width=4)))
    fig_evo.update_layout(title=f"Evolucion: Altas vs Bajas (Años de mayor crecimiento: {', '.join(map(str, top_years))})", 
                        template=TEMPLATE, xaxis_title="Anyo")
    fig_evo.write_html(f"{report_dir}/05_evolucion_temporal.html")

    # --- 3. PROYECTOS ---
    df_prj_counts = df_prj['ESTADO'].value_counts().reset_index()
    df_prj_counts.columns = ['Estado', 'Total']
    fig_prj_pie = px.pie(df_prj_counts, values='Total', names='Estado', title="Estado de Proyectos", 
                     color='Estado', color_discrete_map={'Activo': GREEN, 'Cesado': AMBER})
    fig_prj_pie.write_html(f"{report_dir}/06_proyectos_estado.html")

    df_loc = df_prj.groupby('TX_LUGAR').size().reset_index()
    df_loc.columns = ['Sede', 'Total']
    fig_loc = px.bar(df_loc.sort_values('Total', ascending=False), x='Sede', y='Total', 
                 title="Proyectos por Sede Geografica", color='Total', template=TEMPLATE)
    fig_loc.write_html(f"{report_dir}/07_proyectos_sedes.html")

    # --- 4. MIX & OPERATIVA ---
    # Carga de Trabajo (Proyectos por persona activa)
    active_ids = df_emp[df_emp['ESTADO'] == 'Activo']['ID_EMPLEADO']
    df_asg_active = df_asg[df_asg['ID_EMPLEADO'].isin(active_ids)]
    load = df_asg_active.groupby('ID_EMPLEADO').size().reset_index(name='Proyectos')
    fig_load = px.box(load, y="Proyectos", title="Carga de Trabajo: Proyectos por Empleado Activo", 
                  template=TEMPLATE, color_discrete_sequence=[GREEN])
    fig_load.write_html(f"{report_dir}/08_carga_trabajo.html")

    # Top 5 Proyectos Staff
    top_prj = df_asg.groupby('PROYECTO').size().reset_index()
    top_prj.columns = ['Proyecto', 'Staff']
    fig_top_prj = px.bar(top_prj.nlargest(5, 'Staff'), x='Proyecto', y='Staff',
                     title="Top 5 Proyectos con Mayor Personal Asignado", color='Staff', template=TEMPLATE)
    fig_top_prj.write_html(f"{report_dir}/09_top_proyectos_staff.html")

    # --- 5. GRAFICOS ADICIONALES REQUERIDOS ---

    # Histograma de duracion de proyectos
    df_prj_dur = df_prj[df_prj['DURACION_DIAS'].notna() & (df_prj['DURACION_DIAS'] > 0)].copy()
    fig_dur = px.histogram(df_prj_dur, x='DURACION_DIAS', nbins=20,
                           title="Distribucion de la Duracion de los Proyectos (dias)",
                           template=TEMPLATE, color_discrete_sequence=[BLUE])
    fig_dur.update_layout(xaxis_title="Duracion (dias)", yaxis_title="Numero de proyectos")
    fig_dur.write_html(f"{report_dir}/10_duracion_proyectos.html")

    # Distribucion del numero de proyectos por empleado activo
    active_ids = df_emp[df_emp['ESTADO'] == 'Activo']['ID_EMPLEADO']
    df_asg_active = df_asg[df_asg['ID_EMPLEADO'].isin(active_ids)]
    proyectos_por_emp = df_asg_active.groupby('ID_EMPLEADO').size().reset_index(name='NumProyectos')
    dist = proyectos_por_emp['NumProyectos'].value_counts().sort_index().reset_index()
    dist.columns = ['Proyectos asignados', 'Personas']
    dist['Etiqueta'] = dist['Proyectos asignados'].apply(
        lambda n: f"Personas asignadas a {n} proyecto{'s' if n > 1 else ''}: {dist.loc[dist['Proyectos asignados'] == n, 'Personas'].values[0]}"
    )
    fig_dist = px.bar(dist, x='Proyectos asignados', y='Personas',
                      title="Distribucion: Numero de proyectos por empleado activo",
                      template=TEMPLATE, color_discrete_sequence=[GREEN], text='Personas')
    fig_dist.update_traces(textposition='outside')
    fig_dist.update_layout(xaxis_title="Numero de proyectos asignados", yaxis_title="Numero de empleados")
    fig_dist.write_html(f"{report_dir}/11_distribucion_carga_empleados.html")

    # Lista de proyectos sin personas asignadas (deteccion de anomalia)
    proyectos_activos = df_prj[df_prj['ESTADO'] == 'Activo']['ID_PROYECTO']
    proyectos_con_asignacion = df_asg['ID_PROYECTO'].unique()
    sin_asignacion = df_prj[
        (df_prj['ID_PROYECTO'].isin(proyectos_activos)) &
        (~df_prj['ID_PROYECTO'].isin(proyectos_con_asignacion))
    ][['ID_PROYECTO', 'TX_DESCRIPCION', 'TX_LUGAR']].copy()

    if sin_asignacion.empty:
        fig_anomalia = go.Figure()
        fig_anomalia.add_annotation(text="No se detectaron proyectos sin personal asignado",
                                    xref="paper", yref="paper", x=0.5, y=0.5,
                                    showarrow=False, font=dict(size=16, color=GREEN))
        fig_anomalia.update_layout(title="Anomalia: Proyectos sin personas asignadas", template=TEMPLATE)
    else:
        fig_anomalia = go.Figure(data=[go.Table(
            header=dict(values=['ID', 'Descripcion', 'Lugar'],
                        fill_color=RED, font=dict(color='white', size=12), align='left'),
            cells=dict(values=[sin_asignacion['ID_PROYECTO'],
                                sin_asignacion['TX_DESCRIPCION'],
                                sin_asignacion['TX_LUGAR']],
                       fill_color='lavender', align='left')
        )])
        fig_anomalia.update_layout(title=f"Anomalia: {len(sin_asignacion)} proyecto(s) sin personas asignadas")
    fig_anomalia.write_html(f"{report_dir}/12_proyectos_sin_asignacion.html")

    print(f"Reporte ANALITICO TOTAL generado en la carpeta '{report_dir}'")

if __name__ == "__main__":
    generate_full_report()
