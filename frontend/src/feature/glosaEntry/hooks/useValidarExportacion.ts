import { useMutation } from "@tanstack/react-query";
import { validarExportacionGlosas } from "../services/glosasEntry.api";
import type { ExportGlosasPayload } from "../entry.types";

export const useValidarExportacion = () => {
    return useMutation({
        mutationFn: (
            payload: ExportGlosasPayload
        ) => validarExportacionGlosas(payload),
    });
};