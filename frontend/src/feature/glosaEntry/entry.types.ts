export interface Validation {
    confidence: number;
    is_glosa: boolean;
    pages_analyzed: number;
    score: number;
    signals: {
        emisor: {
            found: boolean;
            matches: number;
            strong: boolean;
        };
        glosa: {
            found: boolean;
            matches: number;
            strong: boolean;
        };
        factura: {
            found: boolean;
            matches: number;
            strong: boolean;
        };
        servicios: {
            found: boolean;
            matches: number;
            strong: boolean;
        };
        causas: {
            found: boolean;
            matches: number;
            strong: boolean;
        };
        observaciones: {
            found: boolean;
            matches: number;
            strong: boolean;
        };
    };
    status: string;
    strong_signals: number;
}

export interface GlosaEncabezado {
    factura_raw: string;
    fecha_notificacion: string;
    fecha_radicacion: string;
    numero_factura: string;
    numero_glosa: string;
    tipo_factura: string;
    valor_facturado: number;
    valor_facturado_raw: string;
    valor_glosa: number;
    valor_glosa_raw: string;
}

export interface GlosaResult {
    name: string;
    valid: boolean;
    encabezado?: GlosaEncabezado;
    items?: ItemGlosa[];
    total_items?: number;
    error?: string;
    validation?: Validation;
}

export interface ResponseUploadPDFs {
    success: boolean;
    total: number;
    glosas: GlosaResult[];
}

export interface ItemGlosa {
    codigo_cups_pdf: string;
    codigo_item: string;
    descripcion: string;
    tipo_item: string;
    valor_cobrado: number;
    valor_glosa: number;
    codigo_glosa: string;
    causa_general: string;
    causa_especifica: string;
    descripcion_causa: string;
    es_global: boolean;
    _page: number;
    _row: number;
}



export interface ItemHIS {
    _rownum: number;
    categoria: string;
    codigo_item: string;
    codigo_honorario: string;
    descripcion: string;
    valor: number;
    fuente: string;
    tipo_item: string;
}

export interface ResponseItemsFactura {
    success: boolean;
    numero_factura: string;
    tipo_factura: string;
    total: number;
    items: ItemHIS[];
}

// ================================

export interface SeleccionHIS extends ItemHIS {
    _uid: string;
    valor_editado?: number;
    _itemUid: string;
    _itemDescripcion: string;
    _itemValorGlosa: number;
    _objetivo_causa_especifica: string;
    _objetivo_codigo_glosa: string;
    _objetivo_descripcion_causa: string;
}

export interface ItemGlosaConUid extends ItemGlosa {
    _globalUid: string;
}

export interface ItemHISConUid extends ItemHIS {
    _uid: string;
    valor_editado?: number;
}

export interface PuntoRuta {
    codigo: string;
    empresa: string;
    descripcion: string;
    departamento: string;
}

export interface ResponsePuntosRuta {
    success: boolean;
    total: number;
    puntos: PuntoRuta[];
}

export type DevolucionFlag = "S" | "N";

export interface DevolucionInfo {
    devolucion: DevolucionFlag;
    puntoRuta: PuntoRuta | null;
}

// EXCELL

export interface SeleccionHISExport { 
    uid: string; 
    codigo: string | null; 
    descripcion: string | null; 
    valor: number; 
    valor_original: number; 
    valor_editado?: number; 
    fuente?: string | null; 
} 

export interface GlobalExport { 
    uid: string; 
    codigo_glosa: string | null; 
    descripcion: string | null; 
    causa_especifica: string | null; 
    descripcion_causa: string | null; 
    valor_glosa: number; 
    selecciones_his: SeleccionHISExport[]; 
} 

export interface FacturaExport { 
    id: string; 
    nombre_archivo: string; 
    numero_factura: string; 
    tipo_factura: string; 
    encabezado: GlosaResult["encabezado"]; 
    items: GlosaResult["items"]; 
    globales: GlobalExport[]; 
    devolucion: DevolucionFlag; 
    punto_ruta: PuntoRuta | null; 
    total_glosa: number; 
    total_detallado: number; 
    total_his: number; 
    total_ajustado: number; 
    diferencia: number; 
    cuadra: boolean; 
} 

export interface ExportGlosasPayload { 
    facturas: FacturaExport[]; 
}