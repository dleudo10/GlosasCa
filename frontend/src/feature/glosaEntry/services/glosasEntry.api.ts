import api from "../../../api/axios";
import type { ExportGlosasPayload, PuntoRuta, ResponsePuntosRuta } from "../entry.types";

export const uploadPDFs = async (files: File[]) => {
    const formData = new FormData()

    files.forEach((file) => {
        formData.append("files", file);
    });

    const {data} = await api.post("glosas/upload/", formData);
    return data;
};

export const getItemsBD = async (
    numeroFactura: string,
    tipoFactura: string,
    codigosExcluir: string[]
) => {
    const { data } = await api.post(
        `glosas/factura/${numeroFactura}/items/?tipo=${tipoFactura}`,
        { codigos_excluir: codigosExcluir }
    );
    console.log("data items bd", data);
    return data;
};

export const getPuntosRuta = async (): Promise<PuntoRuta[]> => {
    const { data } = await api.get<ResponsePuntosRuta>("glosas/puntos-ruta/");
    console.log("data puntos ruta", data);
    return data.puntos;
};

export const exportarGlosas = async ( 
    payload: ExportGlosasPayload 
) => { 
    console.log("payload exportarGlosas", payload);
    const response = await api.post( 
        "glosas/exportar/", 
        payload, 
        { 
            responseType: "blob", 
        } 
    ); 
    
    const blob = new Blob( 
        [response.data], 
        { 
            type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
        } 
    ); 
    
    const url = 
        window.URL.createObjectURL(blob); 
        
    const link = 
        document.createElement("a"); 
        
    link.href = url; 
    link.download = 
        `glosas_${new Date().getTime()}.xlsx`; 
        
    document.body.appendChild(link); 
    link.click(); 
    link.remove(); 
    
    window.URL.revokeObjectURL(url); 
    
    return response; 
};