import { useRef, useState } from "react";

interface UploadZoneProps {
    onFilesChange: (files: File[]) => void;
}

const UploadZone = ({ onFilesChange }: UploadZoneProps) => {
    const inputRef = useRef<HTMLInputElement>(null);
    const [isDragging, setIsDragging] = useState(false);

    const handleClick = () => {
        inputRef.current?.click();
    };

    const handleInputChange = (
        event: React.ChangeEvent<HTMLInputElement>
    ) => {
        const selectedFiles = Array.from(event.target.files ?? []);

        onFilesChange(selectedFiles);

        event.target.value = "";
    };

    const handleDragOver = (
        event: React.DragEvent<HTMLDivElement>
    ) => {
        event.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = (
        event: React.DragEvent<HTMLDivElement>
    ) => {
        event.preventDefault();
        setIsDragging(false);
    };

    const handleDrop = (
        event: React.DragEvent<HTMLDivElement>
    ) => {
        event.preventDefault();

        setIsDragging(false);

        const droppedFiles = Array.from(
            event.dataTransfer.files
        );

        onFilesChange(droppedFiles);
    };

    return (
        <div
            onClick={handleClick}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            className={`
                border-2 border-dashed rounded-xl p-5
                flex flex-col items-center space-y-2
                cursor-pointer transition

                ${
                    isDragging
                        ? "border-blue-500 bg-blue-50"
                        : "border-gray-300 bg-gray-50 hover:bg-gray-100"
                }
            `}
        >
            <input
                ref={inputRef}
                className="hidden"
                type="file"
                multiple
                accept="application/pdf"
                onChange={handleInputChange}
            />

            <div className="text-[32px]">
                📋
            </div>

            <p className="text-gray-500 text-[14px] text-center">
                Arrastra el PDF de la glosa aquí o haz clic para seleccionar
            </p>

            <span className="text-xs text-gray-400">
                Máximo 4 archivos · Solo PDF
            </span>
        </div>
    );
};

export default UploadZone;
