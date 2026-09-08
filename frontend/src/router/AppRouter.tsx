import { Suspense } from "react"
import { BrowserRouter, Route, Routes } from "react-router-dom"
import BaseLayout from "../layout/BaseLayout"
import Index from "../feature/glosaEntry/pages/Index"

const AppRouter = () => {
    return (
        <>
            <BrowserRouter>
                <Suspense fallback={<p>Cargando ...</p>}>
                    <Routes>
                        <Route element={<BaseLayout />}>

                            <Route path="/" element={
                                <Index />
                            } />

                        </Route>

                        <Route path="*" element={<p>Pagina no encontrada</p>} />
                    </Routes>
                </Suspense>
            </BrowserRouter>
        </>
    )
}

export default AppRouter