import { useQuery } from "@tanstack/react-query";
import { getPuntosRuta } from "../services/glosasEntry.api";

export const usePuntosRuta = (habilitado: boolean) =>
    useQuery({
        queryKey: ["puntos-ruta"],
        queryFn: getPuntosRuta,
        enabled: habilitado,
        staleTime: 10 * 60 * 1000,
    });