import { useStep } from "../../../context/StepsContext";
import { sumaDetallada } from "../helper/glosaCalculations"; 
import { formatNumber } from "../helper/formatPrice";
import type { DevolucionFlag, GlosaResult, PuntoRuta } from "../entry.types";
// import { useEffect, useRef } from "react";

interface CardInfoProps {
    glosa?: GlosaResult;
    sumaSeleccionada?: number;
    onSeleccionarHIS?: () => void;
    onExportar?: () => void;
    cargandoHIS?: boolean;
    devolucion?: DevolucionFlag;
    onCambiarDevolucion?: (flag: DevolucionFlag) => void;
    puntosRuta?: PuntoRuta[];
    cargandoPuntos?: boolean;
    puntoRutaSeleccionado?: string | null;
    onSeleccionarPuntoRuta?: (codigo: string) => void;
    datosPuntoRuta?: PuntoRuta | null;
}


const CardInfo = ({
    glosa,
    sumaSeleccionada = 0,
    onSeleccionarHIS,
    cargandoHIS,
    devolucion,
    onCambiarDevolucion,
    puntosRuta,
    cargandoPuntos,
    puntoRutaSeleccionado,
    onSeleccionarPuntoRuta,
    datosPuntoRuta,
}: CardInfoProps)  => {
    // const { start, nextStep, setStep } = useStep();
    const { start } = useStep();


    const encabezado = glosa?.encabezado;
    const items = glosa?.items ?? [];

    const totalGlosaPDF = encabezado?.valor_glosa ?? 0;
    const totalDetallado = sumaDetallada(items);
    const totalAjustado = totalDetallado + sumaSeleccionada;
    const diferencia = totalGlosaPDF - totalAjustado;
    const cuadra = Math.abs(diferencia) < 1;

    // const cuadraAnterior = useRef(cuadra);

    // useEffect(() => {
    //     if (!cuadraAnterior.current && cuadra) {
    //         nextStep();
    //     }

    //     if (cuadraAnterior.current && !cuadra) {
    //         setStep(2);
    //     }

    //     cuadraAnterior.current = cuadra;
    // }, [cuadra]);

    return (
        <div className="w-full rounded-2xl bg-white p-4 shadow-sm space-y-4">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="font-bold text-brand-800">
                        Glosa N° {encabezado?.numero_glosa ?? "Sin número"} · {encabezado?.factura_raw ?? "Sin factura"}
                    </h2>
                    <p className="mt-1 text-sm text-gray-500">
                        Fecha de notificación {encabezado?.fecha_notificacion ?? "Sin fecha"}
                    </p>
                </div>
                <button
                    type="button"
                    onClick={start}
                    className="flex items-center gap-2 rounded-xl border border-gray-300 px-4 py-3 text-sm text-gray-700 transition hover:bg-gray-50"
                >
                    <span>←</span> Nueva carga
                </button>
            </div>

            <div className="grid grid-cols-1 overflow-hidden rounded-xl border border-gray-200 md:grid-cols-2 lg:grid-cols-4">
                <div className="border-b border-gray-200 px-4 py-4 md:border-r lg:border-b-0">
                    <p className="text-xs text-gray-500">Total de la glosa según PDF</p>
                    <p className="mt-2 text-2xl font-semibold text-red-600">${formatNumber(totalGlosaPDF)}</p>
                </div>
                <div className="border-b border-gray-200 px-4 py-4 lg:border-r lg:border-b-0">
                    <p className="text-xs text-gray-500">Ítems detallados del PDF</p>
                    <p className="mt-2 text-2xl font-semibold text-brand-800">${formatNumber(totalDetallado)}</p>
                </div>
                <div className="border-b border-gray-200 px-4 py-4 md:border-r lg:border-b-0">
                    <p className="text-xs text-gray-500">Seleccionados de BD</p>
                    <p className="mt-2 text-2xl font-semibold text-brand-800">${formatNumber(sumaSeleccionada)}</p>
                </div>
                <div className="bg-blue-50/70 px-4 py-4">
                    <p className="text-xs text-gray-500">Total ajustado</p>
                    <p className="mt-2 text-2xl font-semibold text-brand-800">${formatNumber(totalAjustado)}</p>
                </div>
            </div>

            <div
                className={`flex items-center justify-center rounded-lg border px-4 py-3 text-sm ${
                    cuadra ? "border-emerald-200 bg-emerald-50 text-emerald-700" : "border-blue-200 bg-blue-50 text-brand-800"
                }`}
            >
                {cuadra ? (
                    <span>✓ Los valores cuadran perfectamente</span>
                ) : (
                    <span>
                        <span className="mr-1 font-semibold">✗</span>
                        Diferencia de ${formatNumber(Math.abs(diferencia))} — Seleccione más ítems de BD
                    </span>
                )}
            </div>

            <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
                <div className="flex flex-col gap-3 text-sm text-gray-600">
                    <div className="flex flex-wrap items-center gap-2">
                        <span>¿Es devolución?</span>
                        <button
                            type="button"
                            onClick={() => onCambiarDevolucion?.("N")}
                            className={`rounded-lg px-4 py-2 text-sm font-medium transition ${
                                devolucion === "N" ? "bg-brand-800 text-white" : "border border-gray-300 bg-white text-gray-700 hover:bg-gray-50"
                            }`}
                        >
                            No
                        </button>
                        <button
                            type="button"
                            onClick={() => onCambiarDevolucion?.("S")}
                            className={`rounded-lg px-4 py-2 text-sm font-medium transition ${
                                devolucion === "S" ? "bg-brand-800 text-white" : "border border-gray-300 bg-white text-gray-700 hover:bg-gray-50"
                            }`}
                        >
                            Sí
                        </button>
                    </div>

                    {devolucion === "S" && (
                        <div className="flex flex-col gap-3 rounded-xl border border-gray-200 bg-gray-50 p-3">
                            <div className="flex items-center gap-2">
                                <span className="min-w-[140px] text-xs text-gray-500">
                                    Punto de ruta destino <span className="text-red-500">*</span>
                                </span>
                                {cargandoPuntos ? (
                                    <span className="text-xs text-gray-400">Cargando puntos de ruta...</span>
                                ) : (
                                    <select
                                        value={puntoRutaSeleccionado ?? ""}
                                        onChange={(e) => onSeleccionarPuntoRuta?.(e.target.value)}
                                        className="w-full flex-1 rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm outline-none focus:border-brand-800 sm:w-auto"
                                    >
                                        <option value="">— Seleccionar punto de ruta —</option>
                                        {puntosRuta?.map((p, idx) => (
                                            <option 
                                                key={idx} 
                                                value={p.codigo}
                                            >
                                                {p.codigo} - {p.descripcion}
                                            </option>
                                        ))}
                                    </select>
                                )}
                            </div>

                            {puntoRutaSeleccionado && (
                                <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                                    <div>
                                        <p className="text-gray-400">Empresa</p>
                                        <p className="font-medium text-gray-700">
                                            {datosPuntoRuta?.empresa || "—"}
                                        </p>
                                    </div>

                                    <div>
                                        <p className="text-gray-400">Sede</p>
                                        <p className="font-medium text-gray-700">
                                            {datosPuntoRuta?.departamento || "—"}
                                        </p>
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>

                <div className="flex flex-col gap-2 items-center sm:flex-row lg:shrink-0">
                    <button
                        type="button"
                        onClick={onSeleccionarHIS}
                        disabled={cargandoHIS}
                        className="flex w-full items-center justify-center gap-2 rounded-xl border border-gray-300 px-4 py-3 text-sm text-gray-700 transition hover:bg-gray-50 disabled:opacity-50 sm:w-auto"
                    >
                        ⚙ {cargandoHIS ? "Cargando..." : "Seleccionar ítems del HIS"}
                    </button>
                    {devolucion === "S" && !puntoRutaSeleccionado && (
                        <p className="mt-1 text-xs text-amber-600">⚠ Seleccione un punto de ruta para poder exportar</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default CardInfo;