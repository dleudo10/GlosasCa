import Card from '../../../components/Card'
import FileSelector from '../components/FileSelector'

const UploadFile = () => {
    return (
        <Card
            title="Subir PDFs de glosas"
            subtitle="Cargue uno o varios PDFs de glosa — maximo 2 archivo PDF"
        >
            <FileSelector />
        </Card>
    )
}

export default UploadFile