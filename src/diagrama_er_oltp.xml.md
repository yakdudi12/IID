<mxfile host="app.diagrams.net" modified="2023-10-24T00:00:00.000Z" agent="Mozilla/5.0" version="22.0.0" type="device">
  <diagram id="oltp-gdelt" name="Diagrama ER OLTP">
    <mxGraphModel dx="1000" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1000" pageHeight="800" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <!-- Entidad: Noticia_Evento -->
        <mxCell id="noticia" value="&lt;b&gt;Noticia_Evento&lt;/b&gt;&lt;br&gt;&lt;hr&gt;PK: GlobalEventID&lt;br&gt;Fecha_Publicacion&lt;br&gt;URL_Noticia&lt;br&gt;Fecha_Adicion&lt;br&gt;FK: UbicacionID" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;align=left;spacingLeft=10;verticalAlign=top;spacingTop=5;" vertex="1" parent="1">
          <mxGeometry x="360" y="280" width="220" height="130" as="geometry" />
        </mxCell>

        <!-- Entidad: Actor -->
        <mxCell id="actor" value="&lt;b&gt;Actor&lt;/b&gt;&lt;br&gt;&lt;hr&gt;PK: ActorID&lt;br&gt;Codigo_Actor&lt;br&gt;Nombre&lt;br&gt;Tipo" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;align=left;spacingLeft=10;verticalAlign=top;spacingTop=5;" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="200" height="110" as="geometry" />
        </mxCell>

        <!-- Entidad Asociativa: Relacion_Evento_Actor -->
        <mxCell id="rel_actor" value="&lt;b&gt;Relacion_Evento_Actor&lt;/b&gt;&lt;br&gt;&lt;hr&gt;PK, FK1: GlobalEventID&lt;br&gt;PK, FK2: ActorID&lt;br&gt;Rol" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;align=left;spacingLeft=10;verticalAlign=top;spacingTop=5;" vertex="1" parent="1">
          <mxGeometry x="360" y="40" width="220" height="100" as="geometry" />
        </mxCell>

        <!-- Entidad: Ubicacion -->
        <mxCell id="ubicacion" value="&lt;b&gt;Ubicacion&lt;/b&gt;&lt;br&gt;&lt;hr&gt;PK: UbicacionID&lt;br&gt;Pais_Codigo&lt;br&gt;Nombre_Ubicacion&lt;br&gt;Latitud&lt;br&gt;Longitud" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;align=left;spacingLeft=10;verticalAlign=top;spacingTop=5;" vertex="1" parent="1">
          <mxGeometry x="720" y="280" width="200" height="130" as="geometry" />
        </mxCell>

        <!-- Entidad: Fuente_Medio -->
        <mxCell id="fuente" value="&lt;b&gt;Fuente_Medio&lt;/b&gt;&lt;br&gt;&lt;hr&gt;PK: FuenteID&lt;br&gt;Dominio&lt;br&gt;Nombre_Medio" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;align=left;spacingLeft=10;verticalAlign=top;spacingTop=5;" vertex="1" parent="1">
          <mxGeometry x="40" y="520" width="200" height="100" as="geometry" />
        </mxCell>

        <!-- Entidad Asociativa: Relacion_Evento_Fuente -->
        <mxCell id="rel_fuente" value="&lt;b&gt;Relacion_Evento_Fuente&lt;/b&gt;&lt;br&gt;&lt;hr&gt;PK, FK1: GlobalEventID&lt;br&gt;PK, FK2: FuenteID" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;align=left;spacingLeft=10;verticalAlign=top;spacingTop=5;" vertex="1" parent="1">
          <mxGeometry x="360" y="520" width="220" height="90" as="geometry" />
        </mxCell>

        <!-- Entidad: Codigo_CAMEO -->
        <mxCell id="cameo" value="&lt;b&gt;Codigo_CAMEO&lt;/b&gt;&lt;br&gt;&lt;hr&gt;PK: CodigoID&lt;br&gt;Codigo_Evento&lt;br&gt;Descripcion&lt;br&gt;Categoria_Base" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;align=left;spacingLeft=10;verticalAlign=top;spacingTop=5;" vertex="1" parent="1">
          <mxGeometry x="720" y="40" width="200" height="110" as="geometry" />
        </mxCell>

        <!-- Entidad Asociativa: Relacion_Evento_CAMEO -->
        <mxCell id="rel_cameo" value="&lt;b&gt;Relacion_Evento_CAMEO&lt;/b&gt;&lt;br&gt;&lt;hr&gt;PK, FK1: GlobalEventID&lt;br&gt;PK, FK2: CodigoID" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;align=left;spacingLeft=10;verticalAlign=top;spacingTop=5;" vertex="1" parent="1">
          <mxGeometry x="720" y="190" width="200" height="80" as="geometry" />
        </mxCell>

        <!-- Conectores (Relaciones) -->
        
        <!-- Noticia <-> Rel_Actor -->
        <mxCell id="edge_noticia_actor" edge="1" parent="1" source="noticia" target="rel_actor" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=none;strokeWidth=2;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Actor <-> Rel_Actor -->
        <mxCell id="edge_actor_rel" edge="1" parent="1" source="actor" target="rel_actor" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=none;strokeWidth=2;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Noticia <-> Ubicacion (1:N) -->
        <mxCell id="edge_noticia_ubicacion" edge="1" parent="1" source="noticia" target="ubicacion" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=none;strokeWidth=2;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Noticia <-> Rel_Fuente -->
        <mxCell id="edge_noticia_fuente" edge="1" parent="1" source="noticia" target="rel_fuente" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=none;strokeWidth=2;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Fuente <-> Rel_Fuente -->
        <mxCell id="edge_fuente_rel" edge="1" parent="1" source="fuente" target="rel_fuente" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=none;strokeWidth=2;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Noticia <-> Rel_CAMEO -->
        <mxCell id="edge_noticia_cameo" edge="1" parent="1" source="noticia" target="rel_cameo" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=none;strokeWidth=2;">
          <mxGeometry relative="1" as="geometry">
             <Array as="points">
              <mxPoint x="640" y="345" />
              <mxPoint x="640" y="230" />
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- CAMEO <-> Rel_CAMEO -->
        <mxCell id="edge_cameo_rel" edge="1" parent="1" source="cameo" target="rel_cameo" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=none;strokeWidth=2;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>