type CardProps = {
    title?: string;
    subtitle?: string;
    action?: React.ReactNode;
    className?: string;
    children: React.ReactNode;
};

const Card = ({
    title,
    subtitle,
    action,
    className = "",
    children,
}: CardProps) => {
    return (
        <div
            className={`overflow-hidden rounded-xl border border-gray-200 bg-white ${className}`}
        >
            {(title || action) && (
                <div
                    className="flex items-start justify-between gap-4 border-b border-gray-50 bg-gray-100 px-6 pt-5 pb-4">
                    <div>
                        {title && (
                            <h2 className=" text-[14px] font-bold leading-[1.3] tracking-[-0.01em] text-brand-600 ">
                                {title}
                            </h2>
                        )}

                        {subtitle && (
                            <p className="mt-0.75 text-[12px] font-normal text-gary-500">
                                {subtitle}
                            </p>
                        )}
                    </div>

                    {action && (
                        <div className="flex shrink-0 items-center gap-2 ">
                            {action}
                        </div>
                    )}
                </div>
            )}

            <div className="px-6 py-5.5">
                {children}
            </div>
        </div>
    );
};

export default Card;