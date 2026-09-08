const CAUSA_LABEL: Record<string, { texto: string; className: string }> = {
    "07": { texto: "Medicamentos",   className: "bg-amber-100 text-amber-700" },
    "06": { texto: "Dispositivos",   className: "bg-blue-100 text-blue-700" },
    "05": { texto: "Derechos sala",  className: "bg-orange-100 text-orange-700" },
    "01": { texto: "Procedimientos", className: "bg-emerald-100 text-emerald-700" },
    "58": { texto: "Procedimientos", className: "bg-emerald-100 text-emerald-700" },
    "61": { texto: "RIPS",           className: "bg-gray-100 text-gray-700" },
};

export const causaInfo = (causaEspecifica: string) => {
    const match = (causaEspecifica || "").match(/(\d+)/);
    const num = match ? match[1].padStart(2, "0").slice(0, 2) : "";
    return CAUSA_LABEL[num] ?? { texto: causaEspecifica || "—", className: "bg-gray-100 text-gray-700" };
};