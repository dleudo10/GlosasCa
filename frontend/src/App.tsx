import { StepProvider } from "./context/StepsContext"
import AppRouter from "./router/AppRouter"

function App() {
    return (
      <StepProvider>
        <AppRouter />
      </StepProvider>
    )
}

export default App
