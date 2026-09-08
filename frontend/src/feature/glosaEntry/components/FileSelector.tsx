import { useState } from "react";

import UploadZone from "./UploadZone";
import { useUploadPDFs } from "../hooks/useUploadPDFs";
import { useStep } from "../../../context/StepsContext";

import type {
    GlosaResult,
    ResponseUploadPDFs,
} from "../entry.types";

function FileSelector() {
    const [files, setFiles] = useState<File[]>([]);
    const [error, setError] = useState<string>("");
    const [invalidFiles, setInvalidFiles] = useState<string[]>([]);

    const [results, setResults] = useState<GlosaResult[]>([]);

    const { mutate, isPending } = useUploadPDFs();
    const { nextStep, setGlosas } = useStep();


    const handleFiles = (newFiles: File[]) => {
        setError("");
        setInvalidFiles([]);

        const invalidFiles = newFiles.filter(
            (file) => file.type !== "application/pdf"
        );

        if (invalidFiles.length > 0) {
            setError("Solo puedes agregar archivos PDF.");
            return;
        }

        setFiles((prevFiles) => {
            const combinedFiles = [...prevFiles, ...newFiles];

            const uniqueFiles = combinedFiles.filter(
                (file, index, array) =>
                    array.findIndex(
                        (f) =>
                            f.name === file.name &&
                            f.lastModified === file.lastModified
                    ) === index
            );

            if (uniqueFiles.length > 4) {
                setError(
                    `Solo puedes seleccionar máximo 4 archivos y estás cargando ${uniqueFiles.length} archivos.`
                );

                return prevFiles;
            }

            return uniqueFiles;
        });
    };

    const handleRemoveFile = (fileToRemove: File) => {
        setFiles((prevFiles) =>
            prevFiles.filter(
                (file) =>
                    !(
                        file.name === fileToRemove.name &&
                        file.lastModified === fileToRemove.lastModified
                    )
            )
        );

        setInvalidFiles((prev) =>
            prev.filter((name) => name !== fileToRemove.name)
        );

        setError("");
    };

    const handleClearFiles = () => {
        setFiles([]);
        setInvalidFiles([]);
        setError("");
    };

    const handleUpload = () => {
        if (files.length === 0) {
            setError("Debes seleccionar al menos un archivo.");
            return;
        }

        setError("");
        setInvalidFiles([]);

        mutate(files, {
            onSuccess: (data: ResponseUploadPDFs) => {
                console.log("Respuesta del backend:", data);

                const glosas = data.glosas;

                setResults(glosas);

                const rejected = glosas
                    .filter((item) => !item.valid)
                    .map((item) => item.name);

                setInvalidFiles(rejected);

                if (rejected.length > 0) {
                    setError(
                        "Hay archivos que no se pueden procesar. Revisa los mensajes de error."
                    );

                    return;
                }

                setGlosas(glosas);

                nextStep();
            },

            onError: (error) => {
                console.error("Error:", error);

                setError(
                    "No fue posible procesar los archivos."
                );
            },
        });
    };

    const fileCount = files.length;

    return (
        <div>
            <UploadZone onFilesChange={handleFiles} />

            {error && (
                <p className="mt-2 text-sm text-red-500">
                    {error}
                </p>
            )}

            <ul className="mt-4 space-y-3">
                {files.map((file) => {
                    const isInvalid = invalidFiles.includes(file.name);

                    const result = results.find(
                        (item) => item.name === file.name
                    );

                    return (
                        <li
                            key={`${file.name}-${file.lastModified}`}
                            className={`rounded-xl border px-6 py-3 ${
                                isInvalid
                                    ? "border-red-500 bg-red-50"
                                    : "border-gray-200 bg-gray-50"
                            }`}
                        >
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-3">
                                    <span className="text-xl">
                                        📄
                                    </span>

                                    <div className="flex flex-col gap-1">
                                        <span className="text-[14px] text-brand-600">
                                            {file.name}
                                        </span>

                                        <span className="text-[10px] text-gray-500">
                                            {(file.size / 1024).toFixed(0)} KB
                                        </span>
                                    </div>
                                </div>

                                <button
                                    type="button"
                                    onClick={() => handleRemoveFile(file)}
                                    disabled={isPending}
                                    className="
                                        text-sm text-gray-400
                                        disabled:cursor-not-allowed
                                        disabled:opacity-50
                                    "
                                >
                                    ✕
                                </button>
                            </div>

                            {isInvalid && result?.error && (
                                <p className="mt-2 text-xs text-red-600">
                                    {result.error}
                                </p>
                            )}
                        </li>
                    );
                })}
            </ul>

            {files.length > 0 && (
                <div className="mt-4 flex flex-col justify-end gap-2 lg:flex-row">
                    <button
                        type="button"
                        disabled={isPending}
                        onClick={handleClearFiles}
                        className="
                            rounded-lg border bg-gray-50 p-3 px-4 text-[13px]
                            disabled:cursor-not-allowed
                            disabled:opacity-50
                        "
                    >
                        Limpiar lista
                    </button>

                    <button
                        type="button"
                        disabled={isPending}
                        onClick={handleUpload}
                        className="
                            rounded-lg border border-brand-800 bg-brand-800 p-3 px-4 text-[13px] text-white
                            disabled:cursor-not-allowed
                            disabled:opacity-50
                        "
                    >
                        {isPending
                            ? "Procesando..."
                            : `Procesar ${fileCount} ${
                                  fileCount === 1
                                      ? "glosa"
                                      : "glosas"
                              }`}
                    </button>
                </div>
            )}
        </div>
    );
}

export default FileSelector;