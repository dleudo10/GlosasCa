import { useMutation } from "@tanstack/react-query";
import { getItemsBD } from "../services/glosasEntry.api";

export const useItemsFactura = () => {
    return useMutation({
        mutationFn: ({
            numeroFactura,
            tipoFactura,
            codigosExcluir,
        }: {
            numeroFactura: string;
            tipoFactura: string;
            codigosExcluir: string[];
        }) => {
            return getItemsBD(numeroFactura, tipoFactura, codigosExcluir)
        },
    });
};