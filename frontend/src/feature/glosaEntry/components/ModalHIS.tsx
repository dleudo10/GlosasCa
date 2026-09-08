import { useEffect, useState } from "react";
import { formatNumber } from "../helper/formatPrice";
import { valorItemHIS } from "../helper/glosaCalculations";
import type { ItemGlosaConUid, ItemHISConUid } from "../entry.types";

interface ModalHISProps {
    open: boolean;
    itemsGlobales: ItemGlosaConUid[];
    globalActivoUid: string | null;
    onCambiarGlobal: (uid: string) => void;
    items: ItemHISConUid[];
    isSeleccionado: (item: ItemHISConUid) => boolean;
    onToggle: (item: ItemHISConUid) => void;
    onActualizarValor: (uid: string, valor: number | undefined) => void;
    itemsUsadosEnOtrosGlobales: string[];
    onLimpiarSeleccion: () => void;
    onConfirmar: () => void;
    onCerrar: () => void;
}

const ModalHIS = ({
    open,
    itemsGlobales,
    globalActivoUid,
    onCambiarGlobal,
    items,
    isSeleccionado,
    onToggle,
    onActualizarValor,
    itemsUsadosEnOtrosGlobales,
    onLimpiarSeleccion,
    onConfirmar,
    onCerrar,
}: ModalHISProps) => {
    const [busqueda, setBusqueda] = useState("");

    useEffect(() => {
        if (!open) return;
        const handler = (e: KeyboardEvent) => e.key === "Escape" && onCerrar();
        window.addEventListener("keydown", handler);
        return () => window.removeEventListener("keydown", handler);
    }, [open, onCerrar]);

    useEffect(() => { 
        if (!open) setBusqueda(""); 
        console.log(itemsGlobales)
    }, [open]);

    if (!open) return null;

    const globalActivo = itemsGlobales.find((g) => g._globalUid === globalActivoUid) ?? itemsGlobales[0];
    const target = Number(globalActivo?.valor_glosa) || 0;

    const seleccionActual = items.filter(isSeleccionado);
    const sumaActual = seleccionActual.reduce((a, i) => a + valorItemHIS(i), 0);
    const diff = target - sumaActual;
    const cuadra = Math.abs(diff) < 1;

    const disponibles = items.filter(
        (i) => isSeleccionado(i) || !itemsUsadosEnOtrosGlobales.includes(i._uid)
    );

    const texto = busqueda.trim().toLowerCase();
    const filtrados = texto
        ? disponibles.filter(
              (i) =>
                  i.codigo_item?.toLowerCase().includes(texto) ||
                  i.descripcion?.toLowerCase().includes(texto) ||
                  i.categoria?.toLowerCase().includes(texto)
          )
        : disponibles;

    const grupos = filtrados.reduce<Record<string, ItemHISConUid[]>>((acc, item) => {
        const g = item.categoria || "Sin categoría";
        (acc[g] ||= []).push(item);
        return acc;
    }, {});

    return (
        <div
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4"
            onClick={(e) => e.target === e.currentTarget && onCerrar()}
        >
            <div className="flex h-[85vh] w-full max-w-3xl flex-col overflow-hidden rounded-2xl bg-white shadow-xl">

                {/* Head */}
                <div className="flex items-start justify-between border-b border-gray-100 px-6 py-4">
                    <div>
                        <h3 className="text-base font-bold text-brand-800">Seleccione los ítems del HIS</h3>
                        <p className="text-xs text-gray-400">Ítems que complementan el ítem glosado activo</p>
                    </div>
                    <button onClick={onCerrar} className="text-gray-400 hover:text-gray-600">✕</button>
                </div>

                {/* Tabs por ítem global */}
                {itemsGlobales.length > 1 && (
                    <div 
                        className="flex overflow-x-auto gap-2 border-b border-gray-100 px-6 py-3"
                    >
                        {itemsGlobales.map((g) => (
                            <button
                                key={g._globalUid}
                                onClick={() => onCambiarGlobal(g._globalUid)}
                                title={g.descripcion}
                                className={`shrink-0 rounded-xl px-3 py-2 text-left text-xs transition ${
                                    g._globalUid === globalActivoUid
                                        ? "bg-brand-800 text-white"
                                        : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                                }`}
                            >
                                <div className="font-semibold">{g.codigo_glosa || g.codigo_cups_pdf || "—"}</div>
                                <div className="max-w-[140px] truncate opacity-80">{g.descripcion}</div>
                            </button>
                        ))}
                    </div>
                )}
                

                {/* Buscador */}
                <div className="border-b border-gray-100 px-6 py-3">
                    <input
                        type="text"
                        value={busqueda}
                        onChange={(e) => setBusqueda(e.target.value)}
                        placeholder="Buscar por código, nombre o categoría..."
                        className="w-full rounded-lg border border-gray-200 px-3 py-2 text-sm outline-none focus:border-brand-800"
                        autoFocus
                    />
                </div>

                {/* Resumen del ítem activo */}
                <div className="grid grid-cols-4 gap-2 border-b border-gray-100 px-6 py-3 text-xs">
                    <div className="col-span-4 mb-2">
                        <p className="text-gray-400">Ítem a cuadrar</p>
                        <div className="flex flex-col gap-1">
                            <p className="font-semibold text-brand-800">{globalActivo?.codigo_cups_pdf || globalActivo?.codigo_glosa || "—"}</p>
                            <p className="truncate text-[11px] text-gray-500" title={globalActivo?.descripcion}>
                                {globalActivo?.descripcion}
                            </p>
                        </div>
                    </div>
                    <div>
                        <p className="text-gray-400">Causa general</p>
                        <p className="font-semibold text-brand-800">{globalActivo?.causa_general || "—"}</p>
                    </div>
                    <div>
                        <p className="text-gray-400">Valor a cuadrar</p>
                        <p className="font-semibold text-red-600">${formatNumber(target)}</p>
                    </div>
                    <div>
                        <p className="text-gray-400">Seleccionado</p>
                        <p className="font-semibold text-brand-800">${formatNumber(sumaActual)}</p>
                    </div>
                    <div>
                        <p className="text-gray-400">Diferencia</p>
                        <p className={`font-semibold ${cuadra ? "text-emerald-600" : "text-red-600"}`}>
                            {cuadra ? "✓ Cuadra" : `$${formatNumber(Math.abs(diff))}`}
                        </p>
                    </div>
                </div>

                {/* Lista */}
                <div className="flex-1 overflow-y-auto px-6 py-3">
                    {items.length === 0 ? (
                        <p className="py-8 text-center text-sm text-gray-400">
                            No se encontraron ítems en el HIS para esta factura.
                        </p>
                    ) : filtrados.length === 0 ? (
                        <p className="py-8 text-center text-sm text-gray-400">Sin resultados para "{busqueda}"</p>
                    ) : (
                        Object.entries(grupos).map(([grupo, itemsGrupo]) => (
                            <div key={grupo} className="mb-4">
                                <div className="mb-2 flex items-center justify-between text-xs font-semibold text-gray-500">
                                    <span>{grupo}</span>
                                    <span>{itemsGrupo.filter(isSeleccionado).length} / {itemsGrupo.length} seleccionados</span>
                                </div>
                                <div className="space-y-2">
                                    {itemsGrupo.map((item) => {
                                        const sel = isSeleccionado(item);
                                        const valorOriginal = item.valor ?? 0;
                                        const valorMostrar = item.valor_editado ?? valorOriginal;
                                        return (
                                            <div
                                                key={item._uid}
                                                className={`flex items-center gap-3 rounded-xl border px-3 py-2 ${
                                                    sel ? "border-brand-800 bg-blue-50/50" : "border-gray-200"
                                                }`}
                                            >
                                                <input
                                                    type="checkbox"
                                                    checked={sel}
                                                    disabled={cuadra && !sel}
                                                    onChange={() => onToggle(item)}
                                                    className="h-4 w-4"
                                                />
                                                <div 
                                                    className={`min-w-0 flex-1 ${
                                                        cuadra && !sel
                                                            ? "cursor-not-allowed opacity-60"
                                                            : "cursor-pointer"
                                                    }`}
                                                    onClick={() => {
                                                        if (cuadra && !sel) return;
                                                        onToggle(item);
                                                    }}
                                                >
                                                    <div className="flex items-center gap-2 text-xs">
                                                        <span className="font-semibold text-brand-800">{item.codigo_item}</span>
                                                        {item.codigo_honorario && item.codigo_honorario !== item.codigo_item && (
                                                            <span className="text-gray-400">Hon: {item.codigo_honorario}</span>
                                                        )}
                                                    </div>
                                                    <p className="truncate text-sm text-gray-700">{item.descripcion}</p>
                                                </div>
                                                <div className="flex items-center gap-1">
                                                    <span className="text-xs text-gray-400">$</span>
                                                    <input
                                                        type="number"
                                                        value={valorMostrar}
                                                        min={0}
                                                        max={valorOriginal}
                                                        onClick={(e) => e.stopPropagation()}
                                                        onChange={(e) => {
                                                            const limitado = Math.min(Number(e.target.value), valorOriginal);
                                                            onActualizarValor(item._uid, limitado);
                                                        }}
                                                        title={`Valor BD: $${formatNumber(valorOriginal)}`}
                                                        className="w-24 rounded border border-gray-200 px-2 py-1 text-right text-xs"
                                                    />
                                                    {item.valor_editado !== undefined &&
                                                        item.valor_editado !== valorOriginal && (
                                                            <span
                                                                className="text-xs text-gray-400 line-through whitespace-nowrap"
                                                                title="Valor original del HIS"
                                                            >
                                                                ${formatNumber(valorOriginal)}
                                                            </span>
                                                        )
                                                    }
                                                </div>
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        ))
                    )}
                </div>

                {/* Footer */}
                <div className="flex items-center justify-between border-t border-gray-100 px-6 py-4">
                    <span className="text-xs text-gray-500">
                        {seleccionActual.length} ítem{seleccionActual.length !== 1 ? "s" : ""} en este objetivo
                    </span>
                    <div className="flex gap-2">
                        <button onClick={onCerrar} className="rounded-xl border border-gray-300 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                            Cancelar
                        </button>
                        {seleccionActual.length > 0 && (
                            <button
                                type="button"
                                onClick={onLimpiarSeleccion}
                                className="rounded-xl border border-red-200 px-4 py-2 text-sm font-semibold text-red-600 transition hover:bg-red-50"
                            >
                                Limpiar selección
                            </button>
                        )}
                        <button
                            onClick={onConfirmar}
                            className={`rounded-xl px-4 py-2 text-sm font-semibold text-white ${
                                cuadra ? "bg-emerald-600 hover:bg-emerald-700" : "bg-brand-800 hover:bg-brand-900"
                            }`}
                        >
                            {cuadra ? "✓ Confirmar — cuadra" : "Confirmar selección"}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ModalHIS;