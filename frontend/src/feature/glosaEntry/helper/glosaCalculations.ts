import type { GlosaResult, ItemGlosa, ItemHIS, SeleccionHIS } from "../entry.types"; 

export const sumaItems = (items: ItemGlosa[] = []) =>
    items.reduce((acc, item) => acc + (Number(item.valor_glosa) || 0), 0);

export const itemsDetallados = (items: ItemGlosa[] = []) =>
    items.filter((item) => !item.es_global);

export const itemsGlobales = (items: ItemGlosa[] = []) =>
    items.filter((item) => item.es_global);

export const sumaDetallada = (items: ItemGlosa[] = []) =>
    sumaItems(itemsDetallados(items));

// ====================================

export const globalUid = (item: ItemGlosa) =>
    `${item.codigo_cups_pdf}_${item._page}_${item._row}`;

export const hisUid = (item: ItemHIS) =>
    `${item.categoria}_${item._rownum}`;

export const valorItemHIS = (item: ItemHIS & { valor_editado?: number }) =>
    item.valor_editado !== undefined ? Number(item.valor_editado) : Number(item.valor) || 0;

export const sumaSeleccionados = (seleccionesPorGlobal: Record<string, SeleccionHIS[]>) =>
    Object.values(seleccionesPorGlobal)
        .flat()
        .reduce((acc, item) => acc + valorItemHIS(item), 0);

// excel

export const calcularEstadoGlosa = ( 
    glosa: GlosaResult, 
    seleccionesPorGlobal: Record<string, SeleccionHIS[]> 
) => { 
    const totalGlosaPDF = Number(glosa.encabezado?.valor_glosa) || 0; 
    const totalDetallado = sumaDetallada(glosa.items ?? []); 
    const totalHIS = sumaSeleccionados(seleccionesPorGlobal); 
    const totalAjustado = totalDetallado + totalHIS; 
    const diferencia = totalGlosaPDF - totalAjustado; 
    const cuadra = Math.abs(diferencia) < 1; 
    
    return { 
        totalGlosaPDF, 
        totalDetallado, 
        totalHIS, 
        totalAjustado, 
        diferencia, 
        cuadra, 
    }; 
};