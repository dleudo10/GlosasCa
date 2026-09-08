import StepBar from '../components/StepBar'
import UploadFile from '../steps/UploadFile'
import { useStep } from '../../../context/StepsContext'
import ReviewItems from '../steps/ReviewItems'

const Index = () => {
    const STEPS: string[] = ['Subir PDF', 'Revisar ítems', 'Seleccionar faltantes', 'Exportar XLS']
    const { step } = useStep();

    return (
        <>
            <div className="mb-4 flex items-end justify-between">
                <div>
                    <h1 className="text-[22px] font-bold leading-[1.2] tracking-[-0.03em] text-gray-900">
                        Sistema de{" "}
                        <span className="text-brand-600">
                            Gestión de Glosas
                        </span>
                    </h1>
                </div>
            </div>
            <StepBar 
                steps={STEPS}
                current={step}
            />
            {step == 0 && <UploadFile />}
            {[1, 2, 3].includes(step) && <ReviewItems />}
        </>
    )
}

export default Index