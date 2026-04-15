import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import ExpenseForm from './pages/ExpenseForm'
import ExpenseList from './pages/ExpenseList'
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
          <Route path="/expenses/:year/:month" element={<ExpenseList />} />
          <Route path="/expenses/:year/:month/new" element={<ExpenseForm />} />
          <Route
            path="/expenses/:year/:month/:id/edit"
            element={<ExpenseForm />}
          />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
