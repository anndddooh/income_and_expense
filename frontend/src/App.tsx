import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Home from './pages/Home'
import IncomeForm from './pages/IncomeForm'
import IncomeList from './pages/IncomeList'

const queryClient = new QueryClient()

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/incomes/:year/:month" element={<IncomeList />} />
          <Route path="/incomes/:year/:month/new" element={<IncomeForm />} />
          <Route
            path="/incomes/:year/:month/:id/edit"
            element={<IncomeForm />}
          />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
