import { useState } from "react";
import type { ItemGlosa, SeleccionHIS } from "../entry.types";
import { formatNumber } from "../helper/formatPrice";
import {
    itemsDetallados,
    itemsGlobales,
    sumaItems,
    valorItemHIS,
    globalUid,
} from "../helper/glosaCalculations";
import { causaInfo } from "../helper/causaLabel";

interface TableProps {
    items?: ItemGlosa[];
    seleccionesPorGlobal?: Record<string, SeleccionHIS[]>;
    onReconstruirItem?: (uid: string) => void;
}

type Tab = "pdf" | "globales" | "his";

const TabButton = ({ label, count, active, onClick }: { label: string; count: number; active: boolean; onClick: () => void }) => (
    <button
        type="button"
        onClick={onClick}
        className={`relative flex h-12 items-center gap-2 px-5 text-sm first:px-1 ${active ? "font-semibold text-brand-800" : "text-gray-400"}`}
    >
        <span>{label}</span>
        <span className={`rounded-full px-2 py-0.5 text-xs font-semibold ${active ? "bg-blue-100 text-brand-800" : "bg-gray-100 text-gray-500"}`}>
            {count}
        </span>
        {active && <span className="absolute bottom-0 left-0 h-0.5 w-full bg-brand-800" />}
    </button>
);

// TablaGlosados: sin cambios respecto a tu versión actual.
const TablaGlosados = ({ items }: { items: ItemGlosa[] }) => (
    <table className="w-full min-w-275 border-collapse">
        <thead>
            <tr className="bg-brand-800 text-left text-xs font-bold uppercase text-white">
                <th className="w-12 px-3 py-3">#</th>
                <th className="px-3 py-3">CUPS / CUM</th>
                <th className="px-3 py-3">Código ítem (XLS)</th>
                <th className="px-3 py-3">Descripción</th>
                <th className="px-3 py-3">Cód. glosa</th>
                <th className="px-3 py-3">Tipo</th>
                <th className="px-3 py-3">Causa</th>
                <th className="px-3 py-3 text-right">Valor glosa</th>
            </tr>
        </thead>
        <tbody className="text-sm text-gray-700">
            {items.length === 0 ? (
                <tr>
                    <td colSpan={8} className="px-3 py-6 text-center text-gray-400">
                        No hay ítems detallados en esta glosa
                    </td>
                </tr>
            ) : (
                items.map((item, idx) => {
                    const causa = causaInfo(item.causa_especifica);
                    return (
                        <tr
                            key={`${item.codigo_cups_pdf}-${item._page}-${item._row}-${idx}`}
                            className={idx % 2 === 0 ? "bg-white hover:bg-gray-50" : "bg-gray-50/50 hover:bg-gray-100"}
                        >
                            <td className="px-3 py-3 text-gray-500">{idx + 1}</td>
                            <td className="px-3 py-3">
                                <span className="rounded bg-gray-100 px-2 py-1 text-xs font-medium text-brand-800">
                                    {item.codigo_cups_pdf || "—"}
                                </span>
                            </td>
                            <td className="px-3 py-3">
                                <span className="rounded bg-blue-50 px-2 py-1 text-xs font-semibold text-brand-800">
                                    {item.codigo_item || "—"}
                                </span>
                            </td>
                            <td className="max-w-[320px] px-3 py-3">
                                <span className="block truncate" title={item.descripcion}>
                                    {item.descripcion || "—"}
                                </span>
                            </td>
                            <td className="px-3 py-3">
                                <span className="rounded bg-blue-50 px-2 py-1 text-xs font-semibold text-brand-800">
                                    {item.codigo_glosa || "—"}
                                </span>
                            </td>
                            <td className="px-3 py-3">
                                <span className="rounded bg-gray-100 px-2 py-1 text-xs font-medium text-gray-700">
                                    {item.tipo_item || "—"}
                                </span>
                            </td>
                            <td className="px-3 py-3">
                                <span className={`inline-flex rounded-full px-3 py-1 text-xs font-medium ${causa.className}`}>
                                    {causa.texto}
                                </span>
                            </td>
                            <td className="px-3 py-3 text-right font-medium">
                                ${formatNumber(item.valor_glosa)}
                            </td>
                        </tr>
                    );
                })
            )}
        </tbody>
        <tfoot>
            <tr className="border-t border-gray-200 bg-gray-50 text-sm font-semibold text-gray-700">
                <td colSpan={7} className="px-3 py-3 text-right">Total ítems detallados del PDF</td>
                <td className="px-3 py-3 text-right">${formatNumber(sumaItems(items))}</td>
            </tr>
        </tfoot>
    </table>
);

const TablaGlobales = ({
    items,
    seleccionesPorItem,
    onReconstruir,
}: {
    items: ItemGlosa[];
    seleccionesPorItem: Record<string, SeleccionHIS[]>;
    onReconstruir?: (uid: string) => void;
}) => (
    <>
        <div className="px-4 pt-4 mb-4">
            <h3 className="text-sm font-semibold text-brand-800">Ítems globales excluidos del PDF</h3>
            <p className="text-xs text-gray-400">Ítems excluidos — Se detallan mediante la selección de ítems del HIS</p>
        </div>

        <table className="w-full min-w-175 border-collapse">
            <thead>
                <tr className="mt-2 bg-brand-800 text-left text-xs font-bold uppercase text-white">
                    <th className="w-12 px-3 py-3">#</th>
                    <th className="px-3 py-3">Código</th>
                    <th className="px-3 py-3">Descripción</th>
                    <th className="px-3 py-3">Causa específica</th>
                    <th className="px-3 py-3 text-right">Valor</th>
                    <th className="px-3 py-3 text-right">HIS asociados</th>
                    <th className="px-3 py-3"></th>
                </tr>
            </thead>
            <tbody className="text-sm text-gray-700">
                {items.length === 0 ? (
                    <tr><td colSpan={7} className="px-3 py-6 text-center text-gray-400">No hay ítems globales en esta glosa</td></tr>
                ) : (
                    items.map((item, idx) => {
                        const uid = globalUid(item);
                        const seleccionItem = seleccionesPorItem[uid] ?? [];
                        const sumaItem = seleccionItem.reduce((a, i) => a + valorItemHIS(i), 0);
                        const cuadraItem = Math.abs(item.valor_glosa - sumaItem) < 1;

                        return (
                            <tr key={uid} className={idx % 2 === 0 ? "bg-white hover:bg-gray-50" : "bg-gray-50/50 hover:bg-gray-100"}>
                                <td className="px-3 py-3 text-gray-500">{idx + 1}</td>
                                <td className="px-3 py-3">
                                    <span className="rounded bg-gray-100 px-2 py-1 text-xs font-medium text-brand-800">
                                        {item.codigo_cups_pdf || "—"}
                                    </span>
                                </td>
                                <td className="max-w-[280px] px-3 py-3">
                                    <span className="block truncate" title={item.descripcion}>{item.descripcion || "—"}</span>
                                </td>
                                <td className="px-3 py-3">
                                    <span className="inline-block max-w-[220px] truncate rounded bg-gray-100 px-2 py-1 text-xs font-medium text-gray-700" title={item.causa_especifica}>
                                        {item.causa_especifica?.slice(0, 24) || "—"}
                                    </span>
                                </td>
                                <td className="px-3 py-3 text-right font-medium">${formatNumber(item.valor_glosa)}</td>
                                <td className="px-3 py-3 text-right">
                                    <span className={`rounded-full px-2 py-1 text-xs font-semibold ${
                                        seleccionItem.length === 0 ? "bg-gray-100 text-gray-500"
                                        : cuadraItem ? "bg-emerald-100 text-emerald-700"
                                        : "bg-amber-100 text-amber-700"
                                    }`}>
                                        {seleccionItem.length} · {cuadraItem ? "✓" : `$${formatNumber(sumaItem)}`}
                                    </span>
                                </td>
                                <td className="px-3 py-3 text-right">
                                    <button
                                        type="button"
                                        onClick={() => onReconstruir?.(uid)}
                                        className="rounded-lg border border-brand-800 px-3 py-1.5 text-xs font-semibold text-brand-800 hover:bg-blue-50"
                                    >
                                        ⚙ Reconstruir
                                    </button>
                                </td>
                            </tr>
                        );
                    })
                )}
            </tbody>
            <tfoot>
                <tr className="border-t border-gray-200 bg-gray-50 text-sm font-semibold text-gray-700">
                    <td colSpan={4} className="px-3 py-3 text-right">Total excluido del PDF</td>
                    <td className="px-3 py-3 text-right">${formatNumber(sumaItems(items))}</td>
                    <td colSpan={2}></td>
                </tr>
            </tfoot>
        </table>
    </>
);

const TablaHIS = ({ items }: { items: SeleccionHIS[] }) => (
    <table className="w-full min-w-225 border-collapse">
        <thead>
            <tr className="bg-brand-800 text-left text-xs font-bold uppercase text-white">
                <th className="px-3 py-3">Código ítem</th>
                <th className="px-3 py-3">Descripción</th>
                <th className="px-3 py-3">Ítem reconstruido</th>
                <th className="px-3 py-3">Fuente</th>
                <th className="px-3 py-3 text-right">Valor</th>
            </tr>
        </thead>
        <tbody className="text-sm text-gray-700">
            {items.length === 0 ? (
                <tr><td colSpan={5} className="px-3 py-6 text-center text-gray-400">Aún no hay ítems seleccionados del HIS.</td></tr>
            ) : (
                items.map((item) => (
                    <tr key={item._uid} className="odd:bg-white even:bg-gray-50/50">
                        <td className="px-3 py-3"><span className="rounded bg-blue-50 px-2 py-1 text-xs font-semibold text-brand-800">{item.codigo_item}</span></td>
                        <td className="max-w-[280px] px-3 py-3 truncate" title={item.descripcion}>{item.descripcion}</td>
                        <td className="max-w-[220px] px-3 py-3 truncate text-xs text-gray-600" title={item._itemDescripcion}>
                            {item._itemDescripcion || item._objetivo_codigo_glosa || "—"}
                        </td>
                        <td className="px-3 py-3 text-xs text-gray-500">{item.fuente}</td>
                        <td className="px-3 py-3 text-right font-medium">${formatNumber(valorItemHIS(item))}</td>
                    </tr>
                ))
            )}
        </tbody>
        <tfoot>
            <tr className="border-t border-gray-200 bg-gray-50 text-sm font-semibold text-gray-700">
                <td colSpan={4} className="px-3 py-3 text-right">Total seleccionados de BD</td>
                <td className="px-3 py-3 text-right">${formatNumber(items.reduce((a, i) => a + valorItemHIS(i), 0))}</td>
            </tr>
        </tfoot>
    </table>
);

const Table = ({ items = [], seleccionesPorGlobal = {}, onReconstruirItem }: TableProps) => {
    const [tab, setTab] = useState<Tab>("pdf");
    const detallados = itemsDetallados(items);
    const globales = itemsGlobales(items);
    const seleccionados = Object.values(seleccionesPorGlobal).flat();

    return (
        <div className="w-full overflow-hidden rounded-2xl bg-white shadow-sm">
            <div className="flex h-12 items-end border-b border-gray-200 px-4">
                <TabButton label="Ítems glosados (PDF)" count={detallados.length} active={tab === "pdf"} onClick={() => setTab("pdf")} />
                <TabButton label="Globales excluidos" count={globales.length} active={tab === "globales"} onClick={() => setTab("globales")} />
                <TabButton label="Ítems del HIS" count={seleccionados.length} active={tab === "his"} onClick={() => setTab("his")} />
            </div>

            <div className="w-full overflow-x-auto">
                {tab === "pdf" && <TablaGlosados items={detallados} />}
                {tab === "globales" && (
                    <TablaGlobales items={globales} seleccionesPorItem={seleccionesPorGlobal} onReconstruir={onReconstruirItem} />
                )}
                {tab === "his" && <TablaHIS items={seleccionados} />}
            </div>
        </div>
    );
};

export default Table;
