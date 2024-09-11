import geopandas as gpd
from shapely.geometry import LineString, Polygon, MultiLineString

# 读取线型 GeoJSON 文件
input_geojson = 'geojson/CN-border-L1.geojson'
gdf = gpd.read_file(input_geojson)

# 将 LineString 转换为 Polygon
def line_to_polygon(geom):
    if isinstance(geom, LineString):
        # 确保 LineString 是闭合的
        if geom.coords[0] != geom.coords[-1]:
            coords = list(geom.coords)
            coords.append(coords[0])
            geom = LineString(coords)
        
        # 仅转换至少四个点的 LineString
        if len(geom.coords) >= 4:
            return Polygon(geom)
        else:
            return geom  # 不满足条件的保持原样
    elif isinstance(geom, MultiLineString):
        # 对于 MultiLineString，合并所有线段并应用相同的逻辑
        lines = [line for line in geom]
        combined = LineString([pt for line in lines for pt in line.coords])
        
        if combined.coords[0] != combined.coords[-1]:
            coords = list(combined.coords)
            coords.append(coords[0])
            combined = LineString(coords)
        
        if len(combined.coords) >= 4:
            return Polygon(combined)
        else:
            return geom  # 不满足条件的保持原样
    else:
        raise TypeError("Geometry must be a LineString or MultiLineString")

# 应用转换
gdf['geometry'] = gdf['geometry'].apply(line_to_polygon)

# 保存为新的 GeoJSON 文件
output_geojson = 'geojson/polygon_geojson.geojson'
gdf.to_file(output_geojson, driver='GeoJSON')
