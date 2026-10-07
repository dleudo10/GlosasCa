import { useEffect, useMemo, useState } from "react";
import { Search, X, Check, Loader2 } from "lucide-react";
import type { ItemHIS, ItemPendienteResolucion } from "../feature/glosaEntry/entry.types";
import { useItemsFactura } from "../feature/glosaEntry/hooks/useItemsFactura";
import { formatNumber } from "../feature/glosaEntry/helper/formatPrice";

interface ModalResolverItemProps {
    open: boolean;
    pendiente: ItemPendienteResolucion | null;

    onSeleccionar: (
        pendiente: ItemPendienteResolucion,
        item: ItemHIS
    ) => void;

    onCerrar: () => void;
}

const ModalResolverItem = ({
    open,
    pendiente,
    onSeleccionar,
    onCerrar,
}: ModalResolverItemProps) => {

    const [items, setItems] = useState<ItemHIS[]>([]);
    const [busqueda, setBusqueda] = useState("");
    const [valorBusqueda, setValorBusqueda] = useState("");

    const {
        mutateAsync: fetchItemsBD,
        isPending: cargandoBD,
    } = useItemsFactura();

    /*
     * ------------------------------------------------------------
     * Cargar los ítems HIS de la factura pendiente
     * ------------------------------------------------------------
     */
    useEffect(() => {

        if (!open || !pendiente) {
            return;
        }

        let cancelado = false;

        const cargarItems = async () => {

            try {

                setItems([]);
                setBusqueda("");
                setValorBusqueda("");

                const data = await fetchItemsBD({
                    numeroFactura: pendiente.numero_factura,
                    tipoFactura: pendiente.tipo_factura,
                    codigosExcluir: [],
                });

                if (!cancelado) {
                    setItems(data.items ?? []);
                }

            } catch (error) {

                console.error(
                    "Error cargando ítems HIS para resolución:",
                    error
                );

                if (!cancelado) {
                    setItems([]);
                }

            }
        };

        cargarItems();

        return () => {
            cancelado = true;
        };

    }, [
        open,
        pendiente?.uid,
        pendiente?.numero_factura,
        pendiente?.tipo_factura,
        fetchItemsBD,
    ]);

    /*
     * ------------------------------------------------------------
     * ESC para cerrar
     * ------------------------------------------------------------
     */
    useEffect(() => {

        if (!open) {
            return;
        }

        const handleKeyDown = (event: KeyboardEvent) => {

            if (event.key === "Escape") {
                onCerrar();
            }

        };

        window.addEventListener(
            "keydown",
            handleKeyDown
        );

        return () => {
            window.removeEventListener(
                "keydown",
                handleKeyDown
            );
        };

    }, [open, onCerrar]);

    /*
     * ------------------------------------------------------------
     * Filtrar y ordenar resultados
     * ------------------------------------------------------------
     *
     * Prioridad:
     *
     * 1. Valor exacto
     * 2. Código
     * 3. Descripción
     * 4. Categoría
     *
     * Esto reproduce el proceso manual que actualmente haces.
     */
    const itemsFiltrados = useMemo(() => {

        if (!pendiente) {
            return [];
        }

        const texto = busqueda
            .trim()
            .toLowerCase();

        const valorObjetivo =
            Number(pendiente.valor_pdf) || 0;

        const valorFiltro =
            valorBusqueda.trim() === ""
                ? null
                : Number(valorBusqueda);

        const filtrados = items.filter((item) => {

            const codigo =
                String(item.codigo_item ?? "")
                    .toLowerCase();

            const descripcion =
                String(item.descripcion ?? "")
                    .toLowerCase();

            const categoria =
                String(item.categoria ?? "")
                    .toLowerCase();

            const coincideTexto =
                !texto ||
                codigo.includes(texto) ||
                descripcion.includes(texto) ||
                categoria.includes(texto);

            const coincideValor =
                valorFiltro === null ||
                Number(item.valor) === valorFiltro;

            return (
                coincideTexto &&
                coincideValor
            );
        });

        /*
         * Los que tienen exactamente el mismo valor
         * de la glosa aparecen primero.
         */
        return [...filtrados].sort((a, b) => {

            const aExacto =
                Number(a.valor) === valorObjetivo;

            const bExacto =
                Number(b.valor) === valorObjetivo;

            if (aExacto && !bExacto) {
                return -1;
            }

            if (!aExacto && bExacto) {
                return 1;
            }

            return 0;
        });

    }, [
        items,
        busqueda,
        valorBusqueda,
        pendiente,
    ]);

    if (!open || !pendiente) {
        return null;
    }

    return (
        <div
            className="fixed inset-0 z-[60] flex items-center justify-center bg-black/50 p-4"
            onClick={(event) => {
                if (
                    event.target ===
                    event.currentTarget
                ) {
                    onCerrar();
                }
            }}
        >

            <div className="flex h-[90vh] w-full max-w-5xl flex-col overflow-hidden rounded-2xl bg-white shadow-2xl">

                {/* ================================================= */}
                {/* HEADER */}
                {/* ================================================= */}

                <div className="flex items-start justify-between border-b border-gray-100 px-6 py-4">

                    <div>

                        <div className="flex items-center gap-2">

                            <h2 className="text-base font-bold text-brand-800">
                                Resolver ítem pendiente
                            </h2>

                            <span className="rounded-full bg-amber-50 px-2.5 py-1 text-[10px] font-semibold text-amber-700">
                                Requiere revisión
                            </span>

                        </div>

                        <p className="mt-1 text-xs text-gray-400">
                            El código del PDF no pudo ser asociado
                            automáticamente con el HIS.
                        </p>

                    </div>

                    <button
                        type="button"
                        onClick={onCerrar}
                        className="rounded-lg p-1.5 text-gray-400 transition hover:bg-gray-100 hover:text-gray-700"
                        title="Cerrar"
                    >
                        <X size={18} />
                    </button>

                </div>

                {/* ================================================= */}
                {/* INFORMACIÓN DEL ÍTEM DEL PDF */}
                {/* ================================================= */}

                <div className="border-b border-gray-100 bg-gray-50/70 px-6 py-4">

                    <div className="grid grid-cols-1 gap-5 md:grid-cols-5">

                        <div>
                            <p className="text-[11px] font-medium text-gray-400">
                                Factura
                            </p>

                            <p className="mt-1 text-sm font-semibold text-brand-800">
                                {pendiente.numero_factura || "—"}
                            </p>
                        </div>

                        <div>
                            <p className="text-[11px] font-medium text-gray-400">
                                Código PDF
                            </p>

                            <p
                                className="mt-1 truncate text-sm font-semibold text-brand-800"
                                title={pendiente.codigo_pdf}
                            >
                                {pendiente.codigo_pdf || "Sin código"}
                            </p>
                        </div>

                        <div>
                            <p className="text-[11px] font-medium text-gray-400">
                                Valor cobrado
                            </p>

                            <p className="mt-1 text-sm font-semibold text-red-600">
                                ${formatNumber(
                                    Number(
                                        pendiente.valor_factura
                                    ) || 0
                                )}
                            </p>
                        </div>

                        <div>
                            <p className="text-[11px] font-medium text-gray-400">
                                Valor glosado
                            </p>

                            <p className="mt-1 text-sm font-semibold text-red-600">
                                ${formatNumber(
                                    Number(
                                        pendiente.valor_pdf
                                    ) || 0
                                )}
                            </p>
                        </div>

                        <div>
                            <p className="text-[11px] font-medium text-gray-400">
                                Código de glosa
                            </p>

                            <p className="mt-1 text-sm font-semibold text-brand-800">
                                {pendiente.codigo_glosa || "—"}
                            </p>
                        </div>

                    </div>

                    <div className="mt-4">

                        <p className="text-[11px] font-medium text-gray-400">
                            Descripción encontrada en el PDF
                        </p>

                        <p
                            className="mt-1 text-sm text-gray-700"
                            title={pendiente.descripcion_pdf}
                        >
                            {pendiente.descripcion_pdf || "Sin descripción"}
                        </p>

                    </div>

                </div>

                {/* ================================================= */}
                {/* FILTROS */}
                {/* ================================================= */}

                <div className="border-b border-gray-100 px-6 py-4">

                    <div className="grid grid-cols-1 gap-3 md:grid-cols-[minmax(0,1fr)_220px]">

                        {/* Búsqueda texto */}

                        <div className="relative">

                            <Search
                                size={16}
                                className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
                            />

                            <input
                                type="text"
                                value={busqueda}
                                onChange={(event) =>
                                    setBusqueda(
                                        event.target.value
                                    )
                                }
                                placeholder="Buscar por código, descripción o categoría..."
                                className="w-full rounded-xl border border-gray-200 py-2.5 pl-9 pr-3 text-sm outline-none transition focus:border-brand-800 focus:ring-1 focus:ring-brand-800"
                            />

                        </div>

                        {/* Búsqueda valor */}

                        <div>

                            <input
                                type="number"
                                min={0}
                                value={valorBusqueda}
                                onChange={(event) =>
                                    setValorBusqueda(
                                        event.target.value
                                    )
                                }
                                placeholder="Filtrar por valor exacto"
                                className="w-full rounded-xl border border-gray-200 px-3 py-2.5 text-sm outline-none transition focus:border-brand-800 focus:ring-1 focus:ring-brand-800"
                            />

                        </div>

                    </div>

                    <div className="mt-2 flex items-center justify-between">

                        <p className="text-[11px] text-gray-400">

                            {cargandoBD
                                ? "Consultando HIS..."
                                : `${itemsFiltrados.length} resultado${itemsFiltrados.length !== 1 ? "s" : ""}`
                            }

                        </p>

                        {valorBusqueda && (
                            <button
                                type="button"
                                onClick={() =>
                                    setValorBusqueda("")
                                }
                                className="text-[11px] font-medium text-brand-800 hover:underline"
                            >
                                Limpiar filtro de valor
                            </button>
                        )}

                    </div>

                </div>

                {/* ================================================= */}
                {/* LISTADO HIS */}
                {/* ================================================= */}

                <div className="flex-1 overflow-y-auto px-6 py-4">

                    {cargandoBD ? (

                        <div className="flex h-full items-center justify-center">

                            <div className="flex flex-col items-center gap-3">

                                <Loader2
                                    size={28}
                                    className="animate-spin text-brand-800"
                                />

                                <p className="text-sm text-gray-500">
                                    Consultando los ítems de la factura...
                                </p>

                            </div>

                        </div>

                    ) : items.length === 0 ? (

                        <div className="flex h-full items-center justify-center">

                            <div className="text-center">

                                <p className="text-sm font-semibold text-gray-600">
                                    No se encontraron ítems en el HIS
                                </p>

                                <p className="mt-1 text-xs text-gray-400">
                                    No existen registros disponibles
                                    para esta factura.
                                </p>

                            </div>

                        </div>

                    ) : itemsFiltrados.length === 0 ? (

                        <div className="flex h-full items-center justify-center">

                            <div className="text-center">

                                <p className="text-sm font-semibold text-gray-600">
                                    No hay coincidencias
                                </p>

                                <p className="mt-1 text-xs text-gray-400">
                                    Intenta cambiar el texto o el valor
                                    utilizado como filtro.
                                </p>

                            </div>

                        </div>

                    ) : (

                        <div className="overflow-hidden rounded-xl border border-gray-200">

                            {/* Cabecera */}

                            <div className="grid grid-cols-[120px_minmax(0,1fr)_150px_70px_110px] gap-3 bg-gray-50 px-4 py-3 text-[10px] font-semibold uppercase tracking-wide text-gray-400">

                                <span>Código</span>

                                <span>Descripción</span>

                                <span>Categoría</span>

                                <span>Tipo</span>

                                <span className="text-right">
                                    Valor
                                </span>

                            </div>

                            {/* Filas */}

                            <div className="divide-y divide-gray-100">

                                {itemsFiltrados.map((item) => {

                                    const esCoincidenciaValor =
                                        Number(item.valor) ===
                                        Number(
                                            pendiente.valor_pdf
                                        );

                                    return (

                                        <button
                                            key={`${item.codigo_item}-${item._rownum}`}
                                            type="button"
                                            onClick={() =>
                                                onSeleccionar(
                                                    pendiente,
                                                    item
                                                )
                                            }
                                            className={`grid w-full grid-cols-[120px_minmax(0,1fr)_150px_70px_110px] items-center gap-3 px-4 py-3 text-left transition hover:bg-blue-50 ${
                                                esCoincidenciaValor
                                                    ? "bg-emerald-50/40"
                                                    : "bg-white"
                                            }`}
                                        >

                                            {/* Código */}

                                            <div className="min-w-0">

                                                <p
                                                    className="truncate text-xs font-semibold text-brand-800"
                                                    title={item.codigo_item}
                                                >
                                                    {item.codigo_item}
                                                </p>

                                                {item.codigo_honorario &&
                                                    item.codigo_honorario !==
                                                        item.codigo_item && (
                                                        <p
                                                            className="mt-0.5 truncate text-[10px] text-gray-400"
                                                            title={item.codigo_honorario}
                                                        >
                                                            Hon:{" "}
                                                            {
                                                                item.codigo_honorario
                                                            }
                                                        </p>
                                                    )}

                                            </div>

                                            {/* Descripción */}

                                            <div className="min-w-0">

                                                <p
                                                    className="truncate text-sm font-medium text-gray-700"
                                                    title={item.descripcion}
                                                >
                                                    {item.descripcion}
                                                </p>

                                            </div>

                                            {/* Categoría */}

                                            <div className="min-w-0">

                                                <span
                                                    className="block truncate text-xs text-gray-500"
                                                    title={item.categoria}
                                                >
                                                    {item.categoria ||
                                                        "Sin categoría"}
                                                </span>

                                            </div>

                                            {/* Tipo */}

                                            <div>

                                                <span
                                                    className={`inline-flex rounded-full px-2 py-1 text-[10px] font-bold ${
                                                        item.tipo_item ===
                                                        "P"
                                                            ? "bg-blue-50 text-blue-700"
                                                            : "bg-purple-50 text-purple-700"
                                                    }`}
                                                >
                                                    {item.tipo_item ||
                                                        "—"}
                                                </span>

                                            </div>

                                            {/* Valor */}

                                            <div className="text-right">

                                                <p
                                                    className={`text-xs font-semibold ${
                                                        esCoincidenciaValor
                                                            ? "text-emerald-600"
                                                            : "text-gray-700"
                                                    }`}
                                                >
                                                    $
                                                    {formatNumber(
                                                        Number(
                                                            item.valor
                                                        ) || 0
                                                    )}
                                                </p>

                                                {esCoincidenciaValor && (
                                                    <p className="mt-0.5 flex items-center justify-end gap-1 text-[9px] font-medium text-emerald-600">
                                                        <Check
                                                            size={10}
                                                        />
                                                        Valor coincide
                                                    </p>
                                                )}

                                            </div>

                                        </button>

                                    );
                                })}

                            </div>

                        </div>

                    )}

                </div>

                {/* ================================================= */}
                {/* FOOTER */}
                {/* ================================================= */}

                <div className="flex items-center justify-between border-t border-gray-100 px-6 py-4">

                    <div>

                        <p className="text-xs text-gray-500">
                            Selecciona el registro HIS que corresponde
                            al ítem del PDF.
                        </p>

                        <p className="mt-0.5 text-[10px] text-gray-400">
                            El tipo P/S proviene directamente del HIS.
                        </p>

                    </div>

                    <button
                        type="button"
                        onClick={onCerrar}
                        className="rounded-xl border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50"
                    >
                        Cancelar
                    </button>

                </div>

            </div>

        </div>
    );
};

export default ModalResolverItem;