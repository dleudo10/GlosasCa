import { useMutation } from "@tanstack/react-query";
import { uploadPDFs } from "../services/glosasEntry.api";

export const useUploadPDFs = () => {
    return useMutation({
        mutationFn: uploadPDFs,
    });
};
