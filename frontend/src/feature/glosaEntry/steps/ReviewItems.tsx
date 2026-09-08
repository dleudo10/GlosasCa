import CardInfo from "../components/CardInfo";
import Table from "../components/Table";
import ModalHIS from "../components/ModalHIS";
import { useStep } from "../../../context/StepsContext";
import { useRef, useState } from "react";
import { formatNumber } from "../helper/formatPrice";
import {
    sumaDetallada,
    itemsGlobales,
    globalUid,
    hisUid,
    sumaSeleccionados,
    calcularEstadoGlosa,
    valorItemHIS,
} from "../helper/glosaCalculations";
import { useItemsFactura } from "../hooks/useItemsFactura";
import { usePuntosRuta } from "../hooks/usePuntosRuta";

import type {
    ItemGlosaConUid,
    ItemHISConUid,
    SeleccionHIS,
    DevolucionFlag,
    DevolucionInfo,
    ExportGlosasPayload,
    FacturaExport,
    GlobalExport,
    SeleccionHISExport,
    ItemHIS,
} from "../entry.types";
import { exportarGlosas } from "../services/glosasEntry.api";

const ReviewItems = () => {
    // MENSAJE DE ERROR
    const { glosas, nextStep } = useStep();
    const [exportando, setExportando] = useState(false);

    const [selectedGlosa, setSelectedGlosaState] = useState<string | null>(
        glosas[0]?.name ?? null
    );

    // seleccionesPorGlosa: { [nombreGlosa]: { [itemUid]: SeleccionHIS[] } }
    const [seleccionesPorGlosa, setSeleccionesPorGlosa] = useState<
        Record<string, Record<string, SeleccionHIS[]>>
    >({});

    // itemsBDPorGlosa: { [nombreGlosa]: ItemHISConUid[] } — CACHÉ por
    // factura. Se pide UNA sola vez por factura y nunca se sobreescribe
    // al reabrir el modal, así el valor_editado nunca se pierde.
    const [itemsBDPorGlosa, setItemsBDPorGlosa] = useState<
        Record<string, ItemHISConUid[]>
    >({});

    const [devolucionesPorGlosa, setDevolucionesPorGlosa] = useState<
        Record<string, DevolucionInfo>
    >({});

    const [globalActivoUid, setGlobalActivoUid] = useState<string | null>(null);
    const [modalOpen, setModalOpen] = useState(false);

    const { mutateAsync: fetchItemsBD, isPending: cargandoBD } = useItemsFactura();

    const selectedGlosaData = glosas.find((glosa) => glosa.name === selectedGlosa);

    const obtenerEstadoGlosa = (nombreGlosa: string) => { 
        const glosa = glosas.find( (item) => item.name === nombreGlosa ); 
        if (!glosa) { 
            return { 
                totalGlosaPDF: 0, 
                totalDetallado: 0, 
                totalHIS: 0, 
                totalAjustado: 0, 
                diferencia: 0, 
                cuadra: false, 
                rutaValida: false, 
                lista: false, 
            }; 
        } 
        const selecciones = seleccionesPorGlosa[nombreGlosa] ?? {}; 
        const estado = calcularEstadoGlosa( glosa, selecciones ); 
        const devolucion = devolucionesPorGlosa[nombreGlosa]?.devolucion ?? "N"; 
        const puntoRuta = devolucionesPorGlosa[nombreGlosa]?.puntoRuta ?? null; 
        const rutaValida = devolucion !== "S" || Boolean(puntoRuta); 
        
        return { 
            ...estado, 
            rutaValida, 
            lista: estado.cuadra && rutaValida, 
        }; 
    };

    const estadosGlosas = glosas.map((glosa) => ({ 
        nombre: glosa.name, 
        ...obtenerEstadoGlosa(glosa.name), 
    })); 
    
    const puedeExportar = glosas.length > 0 && estadosGlosas.every((glosa) => glosa.lista);

    const seleccionesPorGlobal = selectedGlosa
        ? seleccionesPorGlosa[selectedGlosa] ?? {}
        : {};

    const itemsBD: ItemHISConUid[] = selectedGlosa
        ? itemsBDPorGlosa[selectedGlosa] ?? []
        : [];

    const devolucionInfo: DevolucionInfo = selectedGlosa
        ? devolucionesPorGlosa[selectedGlosa] ?? { devolucion: "N", puntoRuta: null }
        : { devolucion: "N", puntoRuta: null };

    const { data: puntosRuta, isFetching: cargandoPuntos } = usePuntosRuta(
        devolucionInfo.devolucion === "S"
    );
    

    const globalesConUid: ItemGlosaConUid[] = (
        selectedGlosaData?.items ? itemsGlobales(selectedGlosaData.items) : []
    ).map((item) => ({ ...item, _globalUid: globalUid(item) }));

    // ── Cambiar de factura activa: limpia solo el ítem activo y el
    //    modal. Selecciones, caché de HIS y devolución quedan intactas,
    //    indexadas por nombre de glosa — no se mezclan entre facturas.
    const seleccionarGlosa = (nombreGlosa: string) => {
        setSelectedGlosaState(nombreGlosa);
        setGlobalActivoUid(null);
        setModalOpen(false);
    };

    const setSeleccionesGlosaActual = (
        updater: (prev: Record<string, SeleccionHIS[]>) => Record<string, SeleccionHIS[]>
    ) => {
        if (!selectedGlosa) return;
        setSeleccionesPorGlosa((prev) => ({
            ...prev,
            [selectedGlosa]: updater(prev[selectedGlosa] ?? {}),
        }));
    };

    const setDevolucionGlosaActual = (
        updater: (prev: DevolucionInfo) => DevolucionInfo
    ) => {
        if (!selectedGlosa) return;
        setDevolucionesPorGlosa((prev) => ({
            ...prev,
            [selectedGlosa]: updater(prev[selectedGlosa] ?? { devolucion: "N", puntoRuta: null }),
        }));
    };

    // ── Abrir modal: solo pide los ítems del HIS la PRIMERA vez que se
    //    abre para esta factura. Las siguientes veces reutiliza el
    //    caché — con lo cual valor_editado nunca se pierde.
    const hisModalAbiertaAntes = useRef(false);
    
    const abrirModal = async (uidObjetivo?: string) => {
        if (!selectedGlosaData?.encabezado || !selectedGlosaData.items || !selectedGlosa) return;
        if (globalesConUid.length === 0) return;

        // Primera vez que se abre la modal HIS
        if (!hisModalAbiertaAntes.current) {
            hisModalAbiertaAntes.current = true;
            nextStep();
        }

        if (!itemsBDPorGlosa[selectedGlosa]) {
            const { numero_factura, tipo_factura } = selectedGlosaData.encabezado;

            const codigosExcluir = [
                ...selectedGlosaData.items
                    .filter((i) => !i.es_global)
                    .map((i) => i.codigo_cups_pdf?.toUpperCase()),
                ...selectedGlosaData.items.map((i) => i.codigo_item?.toUpperCase()),
                ...selectedGlosaData.items
                    .filter((i) => i.es_global)
                    .map((i) => i.codigo_cups_pdf?.toUpperCase()),
            ].filter((v): v is string => Boolean(v));

            const codigosUnicos = codigosExcluir.filter(
                (v, i, arr) => arr.indexOf(v) === i
            );

            const data = await fetchItemsBD({
                numeroFactura: numero_factura,
                tipoFactura: tipo_factura,
                codigosExcluir: codigosUnicos,
            });

            setItemsBDPorGlosa((prev) => ({
                ...prev,
                [selectedGlosa]: data.items.map((item: ItemHIS) => ({
                    ...item,
                    _uid: hisUid(item),
                })),
            }));
        }

        setGlobalActivoUid(
            uidObjetivo ??
            globalActivoUid ??
            globalesConUid[0]?._globalUid ??
            null
        );

        setModalOpen(true);
    };



    const isSeleccionado = (item: ItemHISConUid) =>
        (seleccionesPorGlobal[globalActivoUid ?? ""] ?? []).some(
            (s) => s._uid === item._uid
        );

    // const toggleItem = (item: ItemHISConUid) => {
    //     if (!globalActivoUid) return;
    //     const globalActivo = globalesConUid.find((g) => g._globalUid === globalActivoUid);
    //     if (!globalActivo) return;

    //     setSeleccionesGlosaActual((prev) => {
    //         const actuales = prev[globalActivoUid] ?? [];
    //         const yaEsta = actuales.find((s) => s._uid === item._uid);

    //         const nuevos: SeleccionHIS[] = yaEsta
    //             ? actuales.filter((s) => s._uid !== item._uid)
    //             : [
    //                   ...actuales,
    //                   {
    //                       ...item,
    //                       _itemUid: globalActivo._globalUid,
    //                       _itemDescripcion: globalActivo.descripcion,
    //                       _itemValorGlosa: globalActivo.valor_glosa,
    //                       _objetivo_causa_especifica: globalActivo.causa_especifica,
    //                       _objetivo_codigo_glosa: globalActivo.codigo_glosa,
    //                       _objetivo_descripcion_causa: globalActivo.descripcion_causa,
    //                   },
    //               ];

    //         return { ...prev, [globalActivoUid]: nuevos };
    //     });
    // };

    const toggleItem = (item: ItemHISConUid) => {
        if (!globalActivoUid) return;

        const globalActivo = globalesConUid.find(
            (g) => g._globalUid === globalActivoUid
        );

        if (!globalActivo) return;

        setSeleccionesGlosaActual((prev) => {
            const actuales = prev[globalActivoUid] ?? [];

            const yaEsta = actuales.some(
                (s) => s._uid === item._uid
            );

            // ─────────────────────────────────────
            // Si ya está seleccionado:
            // SIEMPRE permitimos quitarlo
            // ─────────────────────────────────────
            if (yaEsta) {
                return {
                    ...prev,
                    [globalActivoUid]: actuales.filter(
                        (s) => s._uid !== item._uid
                    ),
                };
            }

            // ─────────────────────────────────────
            // Calcular total actual
            // ─────────────────────────────────────
            const sumaActual = actuales.reduce(
                (total, seleccionado) =>
                    total + valorItemHIS(seleccionado),
                0
            );

            const target =
                Number(globalActivo.valor_glosa) || 0;

            // ─────────────────────────────────────
            // Si ya cuadra o se pasó,
            // NO permitimos agregar otro
            // ─────────────────────────────────────
            if (sumaActual >= target) {
                return prev;
            }

            // ─────────────────────────────────────
            // Agregar nuevo item
            // ─────────────────────────────────────
            return {
                ...prev,
                [globalActivoUid]: [
                    ...actuales,
                    {
                        ...item,
                        _itemUid: globalActivo._globalUid,
                        _itemDescripcion: globalActivo.descripcion,
                        _itemValorGlosa: globalActivo.valor_glosa,
                        _objetivo_causa_especifica:
                            globalActivo.causa_especifica,
                        _objetivo_codigo_glosa:
                            globalActivo.codigo_glosa,
                        _objetivo_descripcion_causa:
                            globalActivo.descripcion_causa,
                    },
                ],
            };
        });
    };

    const limpiarSeleccion = () => {
        if (!globalActivoUid) return;

        setSeleccionesGlosaActual((prev) => ({
            ...prev,
            [globalActivoUid]: [],
        }));
    };

    // ── Actualiza el valor tanto en el CACHÉ (itemsBDPorGlosa, para que
    //    sobreviva a cerrar/reabrir la modal) como en la selección
    //    activa (para que el total y el XLS usen el valor correcto).
    const actualizarValor = (uid: string, nuevoValor: number | undefined) => {
        if (!selectedGlosa) return;

        setItemsBDPorGlosa((prev) => ({
            ...prev,
            [selectedGlosa]: (prev[selectedGlosa] ?? []).map((i) =>
                i._uid === uid ? { ...i, valor_editado: nuevoValor } : i
            ),
        }));

        if (!globalActivoUid) return;
        setSeleccionesGlosaActual((prev) => {
            const actuales = prev[globalActivoUid] ?? [];
            if (!actuales.some((s) => s._uid === uid)) return prev;
            return {
                ...prev,
                [globalActivoUid]: actuales.map((s) =>
                    s._uid === uid ? { ...s, valor_editado: nuevoValor } : s
                ),
            };
        });
    };

    const itemsUsadosEnOtrosGlobales = Object.entries(seleccionesPorGlobal)
        .filter(([uid]) => uid !== globalActivoUid)
        .flatMap(([, arr]) => arr.map((i) => i._uid));

    // ── Puntos de ruta ──────────────────────────────────────────────
    const cambiarDevolucion = (flag: DevolucionFlag) => {
        setDevolucionGlosaActual((prev) => ({
            devolucion: flag,
            puntoRuta: flag === "N" ? null : prev.puntoRuta,
        }));
    };

    const seleccionarPuntoRuta = async (codigo: string) => {
        if (!codigo) {
            setDevolucionGlosaActual((prev) => ({ ...prev, puntoRuta: null }));
            return;
        }
        const punto = puntosRuta?.find((p) => p.codigo === codigo);
        if (!punto) return;

        setDevolucionGlosaActual((prev) => ({
            ...prev,
            puntoRuta: punto,
        }));
    };

    const construirPayloadExportacion = (): ExportGlosasPayload => { 
        const facturas: FacturaExport[] = glosas.map((glosa) => { 
            const nombreGlosa = glosa.name; 
            const selecciones = seleccionesPorGlosa[nombreGlosa] ?? {}; 
            const devolucionInfo = devolucionesPorGlosa[nombreGlosa] ?? { devolucion: "N", puntoRuta: null, }; 
            const estado = calcularEstadoGlosa( glosa, selecciones ); 
            const globales: GlobalExport[] = itemsGlobales(glosa.items ?? []).map( (global) => { 
                const uid = globalUid(global); 
                const seleccionados = selecciones[uid] ?? []; 
                const seleccionesHIS: SeleccionHISExport[] = seleccionados.map((item) => ({ 
                    uid: item._uid, 
                    codigo: item.codigo_item ?? null, 
                    descripcion: item.descripcion ?? null, 
                    valor: valorItemHIS(item), 
                    valor_original: Number(item.valor) || 0, 
                    valor_editado: item.valor_editado, 
                    fuente: item.fuente ?? null, 
                })); 
                
                return { 
                    uid, 
                    codigo_glosa: global.codigo_glosa ?? null, 
                    descripcion: global.descripcion ?? null, 
                    causa_especifica: global.causa_especifica ?? null, 
                    descripcion_causa: global.descripcion_causa ?? null, 
                    valor_glosa: Number(global.valor_glosa) || 0, 
                    selecciones_his: seleccionesHIS, 
                }; 
            } ); 
            
            return { 
                id: nombreGlosa, 
                nombre_archivo: nombreGlosa, 
                numero_factura: glosa.encabezado?.numero_factura ?? "", 
                tipo_factura: glosa.encabezado?.tipo_factura ?? "", 
                encabezado: glosa.encabezado, items: glosa.items ?? [], 
                globales, 
                devolucion: devolucionInfo.devolucion, 
                punto_ruta: devolucionInfo.puntoRuta, 
                total_glosa: estado.totalGlosaPDF, 
                total_detallado: estado.totalDetallado, 
                total_his: estado.totalHIS, 
                total_ajustado: estado.totalAjustado, 
                diferencia: estado.diferencia, 
                cuadra: estado.cuadra, 
            }; 
        }); 
        
        return { facturas, }; 
    };

    const handleExportar = async () => { 
        if (!puedeExportar) { 
            return; 
        } 
        
        try { 
            setExportando(true); 
            const payload = 
                construirPayloadExportacion(); 
                
            await exportarGlosas(payload); 
            
        } catch (error) { 
            console.error( "Error exportando glosas:", error ); 
        } finally { setExportando(false); } };


    return (
        <div className="w-full">
            <div className="grid grid-cols-1 gap-4 lg:grid-cols-[250px_minmax(0,1fr)]">
                <aside className="min-w-0">
                    <div className="mb-3 rounded-2xl bg-white px-4 py-3 shadow-sm">
                        <h2 className="text-sm font-semibold text-brand-800">Glosas cargadas</h2>
                        <p className="mt-1 text-xs text-gray-400">
                            {glosas.length} {glosas.length === 1 ? "archivo" : "archivos"}
                        </p>
                    </div>

                    <div className="flex gap-3 overflow-x-auto pb-2 lg:flex-col lg:overflow-x-visible lg:pb-0">
                        {glosas.map((glosa) => {
                            const isSelected = selectedGlosa === glosa.name;
                            const encabezado = glosa.encabezado;

                            return (
                                <button
                                    key={glosa.name}
                                    type="button"
                                    onClick={() => seleccionarGlosa(glosa.name)}
                                    className={`
                                        min-w-[250px] shrink-0 rounded-2xl px-4 py-3 text-left
                                        shadow-sm transition-all duration-200 hover:shadow-md lg:min-w-0
                                        ${isSelected ? "bg-brand-800 shadow-md" : "bg-white hover:bg-gray-50"}
                                    `}
                                >
                                    <div className="flex items-center justify-between gap-2">
                                        <h3 className={`text-xs font-bold ${isSelected ? "text-white" : "text-brand-800"}`}>
                                            {encabezado?.numero_factura ?? "Sin factura"}
                                        </h3>
                                        <span className={`rounded-full px-3 py-1 text-[11px] font-semibold ${isSelected ? "bg-emerald-100 text-emerald-700" : "bg-emerald-50 text-emerald-600"}`}>
                                            Listo
                                        </span>
                                    </div>
                                    <p className={`mt-2 truncate text-[11px] ${isSelected ? "text-blue-100" : "text-gray-500"}`} title={glosa.name}>
                                        {glosa.name}
                                    </p>
                                    <div className="mt-3 space-y-1.5">
                                        <div className="flex items-center justify-between text-xs">
                                            <span className={isSelected ? "text-blue-100" : "text-gray-400"}>Total PDF</span>
                                            <span className={`font-semibold ${isSelected ? "text-red-300" : "text-red-600"}`}>
                                                {encabezado?.valor_glosa != null ? `$${formatNumber(encabezado.valor_glosa)}` : "Sin valor total"}
                                            </span>
                                        </div>
                                        <div className="flex items-center justify-between text-xs">
                                            <span className={isSelected ? "text-blue-100" : "text-gray-400"}>Ajustado</span>
                                            <span className={`font-semibold ${isSelected ? "text-emerald-300" : "text-emerald-600"}`}>
                                                {formatNumber(sumaDetallada(glosa.items ?? []))}
                                            </span>
                                        </div>
                                    </div>
                                </button>
                            );
                        })}
                    </div>
                </aside>

                <main className="min-w-0 space-y-4">
                    <CardInfo
                        glosa={selectedGlosaData}
                        sumaSeleccionada={sumaSeleccionados(seleccionesPorGlobal)}
                        onSeleccionarHIS={() => abrirModal()}
                        cargandoHIS={cargandoBD}
                        devolucion={devolucionInfo.devolucion}
                        onCambiarDevolucion={cambiarDevolucion}
                        puntosRuta={puntosRuta ?? []}
                        cargandoPuntos={cargandoPuntos}
                        puntoRutaSeleccionado={devolucionInfo.puntoRuta?.codigo ?? null}
                        onSeleccionarPuntoRuta={seleccionarPuntoRuta}
                        datosPuntoRuta={devolucionInfo.puntoRuta}
                    />
                    <div className="flex justify-end">
                        <button
                            type="button"
                            onClick={handleExportar}
                            disabled={!puedeExportar || exportando}
                            className={`
                                rounded-xl px-6 py-3 text-sm font-semibold
                                transition
                                ${
                                    puedeExportar && !exportando
                                        ? "bg-brand-800 text-white hover:bg-brand-900"
                                        : "cursor-not-allowed bg-gray-200 text-gray-400"
                                }
                            `}
                        >
                            {exportando
                                ? "Generando XLS..."
                                : puedeExportar
                                    ? `Exportar ${glosas.length} facturas`
                                    : "Completa todas las facturas"}
                        </button>
                    </div>
                    <Table
                        items={selectedGlosaData?.items}
                        seleccionesPorGlobal={seleccionesPorGlobal}
                        onReconstruirItem={(uid) => abrirModal(uid)}
                    />
                </main>
            </div>

            <ModalHIS
                open={modalOpen}
                itemsGlobales={globalesConUid}
                globalActivoUid={globalActivoUid}
                onCambiarGlobal={setGlobalActivoUid}
                items={itemsBD}
                isSeleccionado={isSeleccionado}
                onToggle={toggleItem}
                onActualizarValor={actualizarValor}
                itemsUsadosEnOtrosGlobales={itemsUsadosEnOtrosGlobales}
                onLimpiarSeleccion={limpiarSeleccion}
                onConfirmar={() => setModalOpen(false)}
                onCerrar={() => setModalOpen(false)}
            />
        </div>
    );
};

export default ReviewItems;

