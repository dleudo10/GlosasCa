type StepsBarProps = {
    steps: string[];
    current: number;
};

const StepBar = ({ steps, current }: StepsBarProps) => {
    return (
        <div className="flex items-cent mb-4 bg-white rounded-xl p-2.5 shadow-xs">
            {steps.map((step, i) => {
                const state =
                    i < current
                        ? "done"
                        : i === current
                            ? "active"
                            : "idle";

                return (
                    <div
                        key={i}
                        className="flex flex-1 items-center gap-2.5"
                    >
                        {/* Punto */}
                        <div
                            className={`
                                flex h-7.5 w-7.5 shrink-0
                                items-center justify-center
                                rounded-full
                                border-2
                                text-[11px] font-bold
                                transition-all duration-200

                                ${
                                    state === "done"
                                        ? `
                                            bg-green-600
                                            border-green-400
                                            text-white
                                        `
                                        : state === "active"
                                            ? `
                                                bg-blue-600
                                                border-blue-400
                                                text-white
                                                shadow-[0_0_0_4px_var(--azul-100)]
                                            `
                                            : `
                                                bg-white
                                                border-gray-200
                                                text-gray-400
                                            `
                                }
                            `}
                        >
                            {state === "done" ? (
                                "✓"
                            ) : (
                                <span className="font-mono text-[11px]">
                                    {i + 1}
                                </span>
                            )}
                        </div>

                        {/* Label */}
                        <span
                            className={`
                                whitespace-nowrap
                                text-[12px]
                                font-semibold
                                transition-colors duration-200

                                ${
                                    state === "done"
                                        ? "text-brand-700)"
                                        : state === "active"
                                            ? "text-blue-700"
                                            : "text-gray-400"
                                }
                            `}
                        >
                            {step}
                        </span>

                        {/* Línea */}
                        {i < steps.length - 1 && (
                            <div
                                className={`mx-2.5 h-[1.5px] min-w-4 flex-1
                                    ${
                                        state === "done"
                                            ? "bg-green-400"
                                            : "bg-gray-200"
                                    }
                                `}
                            />
                        )}
                    </div>
                );
            })}
        </div>
    );
};

export default StepBar;