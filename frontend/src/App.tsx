import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import AppLayout from '@/components/AppLayout'
import { Toaster } from '@/components/ui/sonner'
import { TooltipProvider } from '@/components/ui/tooltip'
import AccountRequire from '@/pages/AccountRequire'
import Balance from '@/pages/Balance'
import Dashboard from '@/pages/Dashboard'
import ExpenseForm from '@/pages/ExpenseForm'
import ExpenseList from '@/pages/ExpenseList'
import IncomeForm from '@/pages/IncomeForm'
import IncomeList from '@/pages/IncomeList'
import LoanForm from '@/pages/LoanForm'
import LoanList from '@/pages/LoanList'
import MethodRequire from '@/pages/MethodRequire'

const queryClient = new QueryClient()

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<AppLayout />}>
            <Route path="/" element={<Dashboard />} />
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
            <Route
              path="/account_require/:year/:month"
              element={<AccountRequire />}
            />
            <Route
              path="/method_require/:year/:month"
              element={<MethodRequire />}
            />
          </Route>
        </Routes>
      </BrowserRouter>
      <Toaster richColors position="top-right" />
      </TooltipProvider>
    </QueryClientProvider>
  )
}
