import { Outlet } from "react-router";

const BaseLayout = () => {
    return (
        <div className="min-h-screen">
            <header className="sticky top-0 z-200 border-b border-white/6 bg-linear-to-br from-brand-950 via-brand-900 to-brand-800 shadow-[0_2px_16px_rgba(0,26,77,0.35)]">
                <div className="mx-auto flex h-16 max-w-330 items-center justify-between px-7">
                    <div className="flex items-center gap-3.5">
                        <div className="flex h-10 w-10 shrink-0 items-center justify-center overflow-hidden rounded-lg">
                            <img
                                src="/favicon.png"
                                alt="Clínica Antioquia"
                                className="h-10 w-10 object-contain"
                            />
                        </div>

                        <div className="flex flex-col gap-px">
                            <span className="text-[18px] font-bold leading-[1.2] tracking-[-0.02em] text-white">
                                Clínica Antioquia
                            </span>

                            <span className="text-[13px] font-normal tracking-[0.01em] text-brand-300">
                                Sistema de Gestión de Glosas
                            </span>
                        </div>
                    </div>
                </div>
            </header>
            <main className="mx-auto max-w-375 py-5 px-7">
                <Outlet />
            </main>
        </div>
    )
}


export default BaseLayout