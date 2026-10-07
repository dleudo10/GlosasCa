import { useEffect, useMemo, useState } from "react";
import { formatNumber } from "../feature/glosaEntry/helper/formatPrice";
import { useItemsFactura } from "../feature/glosaEntry/hooks/useItemsFactura";
import type {
    ItemHIS,
    ItemPendienteResolucion,
    ResolucionDetalle,
} from "../feature/glosaEntry/entry.types";

interface ModalResolverItemProps {
    open: boolean;
    pendientes: ItemPendienteResolucion[];
    pendienteActivoUid: string | null;
    onCambiarPendiente: (uid: string) => void;
    /** Selección guardada por uid de pendiente (cache en el padre) */
    resoluciones: Record<string, ResolucionDetalle>;
    /** item = null → quitar selección */
    onSeleccionar: (pendiente: ItemPendienteResolucion, item: ItemHIS | null) => void;
    onActualizarValor: (uid: string, valor: number | undefined) => void;
    onLimpiarSeleccion: (uid: string) => void;
    onConfirmar: () => void;
    onCerrar: () => void;
}

const itemId = (i: ItemHIS) => `${i.codigo_item}-${i._rownum}`;
const claveFactura = (p: ItemPendienteResolucion) => `${p.numero_factura}|${p.tipo_factura}`;

const ModalResolverItem = ({
    open,
    pendientes,
    pendienteActivoUid,
    onCambiarPendiente,
    resoluciones,
    onSeleccionar,
    onActualizarValor,
    onLimpiarSeleccion,
    onConfirmar,
    onCerrar,
}: ModalResolverItemProps) => {
    const [busqueda, setBusqueda] = useState("");
    const [valorBusqueda, setValorBusqueda] = useState("");
    // Caché de ítems HIS por factura: se consulta una sola vez
    const [cacheItems, setCacheItems] = useState<Record<string, ItemHIS[]>>({});
    const { mutateAsync: fetchItemsBD, isPending: cargandoBD } = useItemsFactura();

    const pendiente =
        pendientes.find((p) => p.uid === pendienteActivoUid) ?? pendientes[0] ?? null;
    const clave = pendiente ? claveFactura(pendiente) : null;
    const items = clave ? cacheItems[clave] ?? [] : [];

    useEffect(() => {
        if (!open || !pendiente || !clave || cacheItems[clave]) return;
        let cancelado = false;
        (async () => {
            try {
                const data = await fetchItemsBD({
                    numeroFactura: pendiente.numero_factura,
                    tipoFactura: pendiente.tipo_factura,
                    codigosExcluir: [],
                });
                if (!cancelado) {
                    setCacheItems((prev) => ({ ...prev, [clave]: data.items ?? [] }));
                }
            } catch (error) {
                console.error("Error cargando ítems HIS para resolución:", error);
            }
        })();
        return () => {
            cancelado = true;
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [open, clave]);

    // Limpiar filtros al cambiar de pendiente o al cerrar
    useEffect(() => {
        setBusqueda("");
        setValorBusqueda("");
    }, [open, pendienteActivoUid]);

    useEffect(() => {
        if (!open) return;
        const handler = (e: KeyboardEvent) => e.key === "Escape" && onCerrar();
        window.addEventListener("keydown", handler);
        return () => window.removeEventListener("keydown", handler);
    }, [open, onCerrar]);

    const resolucionActual = pendiente ? resoluciones[pendiente.uid] : undefined;
    const itemSeleccionadoId = resolucionActual ? itemId(resolucionActual.item) : null;

    const filtrados = useMemo(() => {
        if (!pendiente) return [];
        const texto = busqueda.trim().toLowerCase();
        const valorFiltro = valorBusqueda.trim() === "" ? null : Number(valorBusqueda);
        const objetivo = Number(pendiente.valor_cobrado ) || 0;

        return items
            .filter((i) => {
                const okTexto =
                    !texto ||
                    String(i.codigo_item ?? "").toLowerCase().includes(texto) ||
                    String(i.descripcion ?? "").toLowerCase().includes(texto) ||
                    String(i.categoria ?? "").toLowerCase().includes(texto);
                const okValor = valorFiltro === null || Number(i.valor) === valorFiltro;
                return okTexto && okValor;
            })
            .sort((a, b) => {
                const ae = Number(a.valor) === objetivo;
                const be = Number(b.valor) === objetivo;
                return ae === be ? 0 : ae ? -1 : 1;
            });
    }, [items, busqueda, valorBusqueda, pendiente]);

    if (!open || !pendiente) return null;

    const target = Number(pendiente.valor_pdf) || 0;
    const cobrado = Number(pendiente.valor_cobrado) || 0;
    // const valorOriginalSel = resolucionActual ? Number(resolucionActual.item.valor) || 0 : 0;
    // const sumaActual = resolucionActual
    //     ? resolucionActual.valor_editado ?? valorOriginalSel
    //     : 0;
    // const diff = target - sumaActual;
    // const cuadra = Boolean(resolucionActual) && Math.abs(diff) < 1;

    const resueltos = pendientes.filter((p) => resoluciones[p.uid]).length;

    const grupos = filtrados.reduce<Record<string, ItemHIS[]>>((acc, item) => {
        const g = item.categoria || "Sin categoría";
        (acc[g] ||= []).push(item);
        return acc;
    }, {});

    return (
        <div
            className="fixed inset-0 z-[60] flex items-center justify-center bg-black/40 p-4"
            onClick={(e) => e.target === e.currentTarget && onCerrar()}
        >
            <div className="flex h-[85vh] w-full max-w-3xl flex-col overflow-hidden rounded-2xl bg-white shadow-xl">
                {/* Head */}
                <div className="flex items-start justify-between border-b border-gray-100 px-6 py-4">
                    <div>
                        <h3 className="text-base font-bold text-brand-800">
                            Resolver ítems pendientes
                        </h3>
                        <p className="text-xs text-gray-400">
                            El código del PDF no pudo asociarse automáticamente con el HIS ·{" "}
                            {resueltos} / {pendientes.length} resueltos
                        </p>
                    </div>
                    <button onClick={onCerrar} className="text-gray-400 hover:text-gray-600">
                        ✕
                    </button>
                </div>

                {/* Tabs por ítem pendiente */}
                {pendientes.length > 1 && (
                    <div className="flex gap-2 overflow-x-auto border-b border-gray-100 px-6 py-3">
                        {pendientes.map((p) => {
                            const activo = p.uid === pendiente.uid;
                            const resuelto = Boolean(resoluciones[p.uid]);
                            return (
                                <button
                                    key={p.uid}
                                    onClick={() => onCambiarPendiente(p.uid)}
                                    title={p.descripcion_pdf}
                                    className={`shrink-0 rounded-xl px-3 py-2 text-left text-xs transition ${
                                        activo
                                            ? "bg-brand-800 text-white"
                                            : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                                    }`}
                                >
                                    <div className="flex items-center gap-1 font-semibold">
                                        {resuelto && <span>✓</span>}
                                        {p.codigo_pdf || p.codigo_glosa || "—"}
                                    </div>
                                    <div className="max-w-[140px] truncate opacity-80">
                                        {p.numero_factura} · {p.descripcion_pdf}
                                    </div>
                                </button>
                            );
                        })}
                    </div>
                )}

            

                {/* Resumen del ítem activo */}
                <div className="grid grid-cols-4 gap-2 border-b border-gray-100 px-6 py-3 text-xs">
                    <div className="col-span-4 mb-2">
                        <p className="text-gray-400">Ítem a resolver </p>
                    </div>
                    <div>
                        <p className="text-gray-400">Factura</p>
                        <p className="font-semibold text-brand-800">{pendiente.numero_factura || "—"}</p>
                    </div>
                    <div>
                        <p className="text-gray-400">Código glosa</p>
                        <p className="font-semibold text-brand-800">{pendiente.codigo_glosa || "—"}</p>
                    </div>
                    <div>
                        <p className="text-gray-400">Valor cobrado</p>
                        <p className="font-semibold text-brand-800">
                            ${formatNumber(Number(pendiente.valor_cobrado) || 0)}
                        </p>
                    </div>
                    <div>
                        <p className="text-gray-400">Valor glosado</p>
                        <p className="font-semibold text-red-600">${formatNumber(target)}</p>
                    </div>
                    <div className="col-span-4 flex flex-col gap-1">
                        <p className="font-semibold text-brand-800">
                            {pendiente.codigo_pdf || "Sin código"}
                        </p>
                        <p
                            className="text-[11px] text-gray-500"
                            title={pendiente.descripcion_pdf}
                        >
                            {pendiente.descripcion_pdf || "Sin descripción"}
                        </p>
                    </div>
                </div>

                {/* Buscadores */}
                <div className="grid grid-cols-[minmax(0,1fr)_180px] gap-2 border-b border-gray-100 px-6 py-3">
                    <input
                        type="text"
                        value={busqueda}
                        onChange={(e) => setBusqueda(e.target.value)}
                        placeholder="Buscar por código, nombre o categoría..."
                        className="w-full rounded-lg border border-gray-200 px-3 py-2 text-sm outline-none focus:border-brand-800"
                        autoFocus
                    />
                    <input
                        type="number"
                        min={0}
                        value={valorBusqueda}
                        onChange={(e) => setValorBusqueda(e.target.value)}
                        placeholder="Valor exacto"
                        className="w-full rounded-lg border border-gray-200 px-3 py-2 text-sm outline-none focus:border-brand-800"
                    />
                </div>

                {/* Lista */}
                <div className="flex-1 overflow-y-auto px-6 py-3">
                    {cargandoBD && items.length === 0 ? (
                        <p className="py-8 text-center text-sm text-gray-400">
                            Consultando los ítems de la factura...
                        </p>
                    ) : items.length === 0 ? (
                        <p className="py-8 text-center text-sm text-gray-400">
                            No se encontraron ítems en el HIS para esta factura.
                        </p>
                    ) : filtrados.length === 0 ? (
                        <p className="py-8 text-center text-sm text-gray-400">
                            Sin resultados con los filtros actuales
                        </p>
                    ) : (
                        Object.entries(grupos).map(([grupo, itemsGrupo]) => (
                            <div key={grupo} className="mb-4">
                                <div className="mb-2 flex items-center justify-between text-xs font-semibold text-gray-500">
                                    <span>{grupo}</span>
                                    <span>{itemsGrupo.length} ítems</span>
                                </div>
                                <div className="space-y-2">
                                    {itemsGrupo.map((item) => {
                                        const id = itemId(item);
                                        const sel = id === itemSeleccionadoId;
                                        const valorOriginal = Number(item.valor) || 0;
                                        const valorMostrar = sel
                                            ? resolucionActual?.valor_editado ?? valorOriginal
                                            : valorOriginal;
                                        const coincide = valorOriginal === cobrado;

                                        return (
                                            <div
                                                key={id}
                                                className={`flex items-center gap-3 rounded-xl border px-3 py-2 ${
                                                    sel
                                                        ? "border-brand-800 bg-blue-50/50"
                                                        : coincide
                                                          ? "border-emerald-200 bg-emerald-50/40"
                                                          : "border-gray-200"
                                                }`}
                                            >
                                                <input
                                                    type="checkbox"
                                                    checked={sel}
                                                    onChange={() =>
                                                        onSeleccionar(pendiente, sel ? null : item)
                                                    }
                                                    className="h-4 w-4"
                                                />
                                                <div
                                                    className="min-w-0 flex-1 cursor-pointer"
                                                    onClick={() =>
                                                        onSeleccionar(pendiente, sel ? null : item)
                                                    }
                                                >
                                                    <div className="flex items-center gap-2 text-xs">
                                                        <span className="font-semibold text-brand-800">
                                                            {item.codigo_item}
                                                        </span>
                                                        {item.codigo_honorario &&
                                                            item.codigo_honorario !== item.codigo_item && (
                                                                <span className="text-gray-400">
                                                                    Hon: {item.codigo_honorario}
                                                                </span>
                                                            )}
                                                        <span
                                                            className={`rounded-full px-2 py-0.5 text-[10px] font-bold ${
                                                                item.tipo_item === "P"
                                                                    ? "bg-blue-50 text-blue-700"
                                                                    : "bg-purple-50 text-purple-700"
                                                            }`}
                                                        >
                                                            {item.tipo_item || "—"}
                                                        </span>
                                                        {coincide && (
                                                            <span className="text-[10px] font-medium text-emerald-600">
                                                                ✓ Valor coincide
                                                            </span>
                                                        )}
                                                    </div>
                                                    <p className="truncate text-sm text-gray-700">
                                                        {item.descripcion}
                                                    </p>
                                                </div>
                                                <div className="flex items-center gap-1">
                                                    <span className="text-xs text-gray-400">$</span>
                                                    <input
                                                        type="number"
                                                        value={valorMostrar}
                                                        min={0}
                                                        max={valorOriginal}
                                                        disabled={!sel}
                                                        onClick={(e) => e.stopPropagation()}
                                                        onChange={(e) => {
                                                            const limitado = Math.min(
                                                                Number(e.target.value),
                                                                valorOriginal
                                                            );
                                                            onActualizarValor(pendiente.uid, limitado);
                                                        }}
                                                        title={`Valor BD: $${formatNumber(valorOriginal)}`}
                                                        className="w-24 rounded border border-gray-200 px-2 py-1 text-right text-xs disabled:bg-gray-50 disabled:text-gray-400"
                                                    />
                                                    {sel &&
                                                        resolucionActual?.valor_editado !== undefined &&
                                                        resolucionActual.valor_editado !== valorOriginal && (
                                                            <span
                                                                className="whitespace-nowrap text-xs text-gray-400 line-through"
                                                                title="Valor original del HIS"
                                                            >
                                                                ${formatNumber(valorOriginal)}
                                                            </span>
                                                        )}
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
                        {resueltos} de {pendientes.length} pendientes resueltos
                    </span>
                    <div className="flex gap-2">
                        <button
                            onClick={onCerrar}
                            className="rounded-xl border border-gray-300 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                        >
                            Cancelar
                        </button>
                        {resolucionActual && (
                            <button
                                type="button"
                                onClick={() => onLimpiarSeleccion(pendiente.uid)}
                                className="rounded-xl border border-red-200 px-4 py-2 text-sm font-semibold text-red-600 transition hover:bg-red-50"
                            >
                                Limpiar selección
                            </button>
                        )}
                        <button
                            onClick={onConfirmar}
                            className={`rounded-xl px-4 py-2 text-sm font-semibold text-white ${
                                resueltos === pendientes.length
                                    ? "bg-emerald-600 hover:bg-emerald-700"
                                    : "bg-brand-800 hover:bg-brand-900"
                            }`}
                        >
                            {resueltos === pendientes.length
                                ? "✓ Confirmar — todo resuelto"
                                : "Guardar y cerrar"}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ModalResolverItem;
