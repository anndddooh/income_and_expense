import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Balance from './pages/Balance'
import ExpenseForm from './pages/ExpenseForm'
import ExpenseList from './pages/ExpenseList'
import Home from './pages/Home'
import IncomeForm from './pages/IncomeForm'
import IncomeList from './pages/IncomeList'
import LoanForm from './pages/LoanForm'
import LoanList from './pages/LoanList'

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
          <Route path="/balance/:year/:month" element={<Balance />} />
          <Route path="/loans/:year/:month" element={<LoanList />} />
          <Route path="/loans/:year/:month/new" element={<LoanForm />} />
          <Route path="/loans/:year/:month/:id/edit" element={<LoanForm />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
