import {
  Box,
  Container,
  HStack,
  SimpleGrid,
  Stat,
  Select,
  Spinner,
} from "@chakra-ui/react"
import { createListCollection } from "@ark-ui/react";
import { createFileRoute } from "@tanstack/react-router"
import { useState, useEffect } from "react"

// Types for API responses
type Transaction = {
  amount_ars: number
  // Add other fields if needed
}

type ApiResponse = {
  data: Transaction[]
  count: number
  pagination: {
    skip: number
    limit: number
  }
}

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
})

function Dashboard() {
  const currentYear = new Date().getFullYear()
  const currentMonth = new Date().getMonth() + 1 // JavaScript months are 0-indexed

  // Using string values throughout to avoid type conversion issues
  const [selectedYear, setSelectedYear] = useState(currentYear.toString())
  const [selectedMonth, setSelectedMonth] = useState(currentMonth.toString())

  // Generate year options
  const years = Array.from({ length: currentYear - 2023 + 1 }, (_, i) => (currentYear - i).toString())
  const months = Array.from({ length: 12 }, (_, i) => (i + 1).toString())

  // Get month name from number
  const getMonthName = (monthNum: string) => {
    return new Date(0, parseInt(monthNum) - 1).toLocaleString("default", { month: "long" })
  }

  // Dashboard stats
  const [income, setIncome] = useState(0)
  const [expenses, setExpenses] = useState(0)
  const [isLoading, setIsLoading] = useState(false)

  // Fetch data when year/month changes
  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true)
      try {
        const year = selectedYear
        const month = selectedMonth.padStart(2, '0')
        const fromDate = `${year}-${month}-01`
        const lastDay = new Date(parseInt(year), parseInt(month), 0)
        const toDate = lastDay.toISOString().slice(0, 10)

        // Fetch income and expenses in parallel
        const [incomeRes, expensesRes] = await Promise.all([
          fetch(`http://localhost:8000/api/v1/income/?from_date=${fromDate}&to_date=${toDate}&currencies=ARS`),
          fetch(`http://localhost:8000/api/v1/expenses/?from_date=${fromDate}&to_date=${toDate}&currencies=ARS`)
        ])

        if (!incomeRes.ok || !expensesRes.ok) {
          throw new Error('Failed to fetch data')
        }

        const [incomeData, expensesData]: [ApiResponse, ApiResponse] = await Promise.all([
          incomeRes.json(),
          expensesRes.json()
        ])

        // Calculate totals
        const totalIncome = incomeData.data.reduce(
          (sum: number, item: Transaction) => sum + (item.amount_ars || 0),
          0
        )
        const totalExpenses = expensesData.data.reduce(
          (sum: number, item: Transaction) => sum + (item.amount_ars || 0),
          0
        )

        setIncome(totalIncome)
        setExpenses(totalExpenses)
      } catch (error) {
        console.error('Error fetching data:', error)
        setIncome(0)
        setExpenses(0)
      } finally {
        setIsLoading(false)
      }
    }

    fetchData()
  }, [selectedYear, selectedMonth])

  return (
    <>
      {/* Year/Month Selectors */}
      <HStack mt={4} mb={8} justifyContent="flex-end" gap={4}>
        {/* Year Selector */}
        <Select.Root 
          value={[selectedYear]}
          onValueChange={(value) => {
            if (Array.isArray(value) && value.length > 0) {
              setSelectedYear(value[0])
            }
          }}
          size="sm"
          collection={createListCollection({
            items: years.map(year => ({ value: year, label: year })),
          })}
        >
          <Select.Control>
            <Select.Trigger>
              <Select.ValueText>{selectedYear}</Select.ValueText>
            </Select.Trigger>
            <Select.IndicatorGroup>
              <Select.Indicator />
            </Select.IndicatorGroup>
          </Select.Control>
        </Select.Root>

        {/* Month Selector */}
        <Select.Root 
          value={[selectedMonth]}
          onValueChange={(value) => {
            if (Array.isArray(value) && value.length > 0) {
              setSelectedMonth(value[0])
            }
          }}
          size="sm"
          collection={createListCollection({
            items: months.map(month => ({ value: month, label: getMonthName(month) })),
          })}
        >
          <Select.Control>
            <Select.Trigger>
              <Select.ValueText>{getMonthName(selectedMonth)}</Select.ValueText>
            </Select.Trigger>
            <Select.IndicatorGroup>
              <Select.Indicator />
            </Select.IndicatorGroup>
          </Select.Control>
        </Select.Root>
      </HStack>

      {/* Rest of your dashboard */}
      <Container maxW="full">
        <Box pt={4} m={4}>
          <SimpleGrid columns={2} gap={10}>
            {/* Income stats */}
            <Stat.Root p={4} borderWidth="1px" borderRadius="lg">
              <Stat.Label>Total Income</Stat.Label>
              <Stat.ValueText>
                {isLoading ? (
                  <Spinner size="sm" />
                ) : (
                  `$ ${income.toLocaleString(undefined, { minimumFractionDigits: 2 })}`
                )}
              </Stat.ValueText>
            </Stat.Root>
            <Stat.Root p={4} borderWidth="1px" borderRadius="lg">
              <Stat.Label>Average Income</Stat.Label>
              <Stat.ValueText>
                {isLoading ? (
                  <Spinner size="sm" />
                ) : (
                  `$ ${(income / new Date(parseInt(selectedYear), parseInt(selectedMonth), 0).getDate()).toLocaleString(undefined, { minimumFractionDigits: 2 })}`
                )}
              </Stat.ValueText>
            </Stat.Root>
            {/* Expense stats */}
            <Stat.Root p={4} borderWidth="1px" borderRadius="lg">
              <Stat.Label>Total Expenses</Stat.Label>
              <Stat.ValueText>
                {isLoading ? (
                  <Spinner size="sm" />
                ) : (
                  `$ ${expenses.toLocaleString(undefined, { minimumFractionDigits: 2 })}`
                )}
              </Stat.ValueText>
            </Stat.Root>
            <Stat.Root p={4} borderWidth="1px" borderRadius="lg">
              <Stat.Label>Average Expenses</Stat.Label>
              <Stat.ValueText>
                {isLoading ? (
                  <Spinner size="sm" />
                ) : (
                  `$ ${(expenses / new Date(parseInt(selectedYear), parseInt(selectedMonth), 0).getDate()).toLocaleString(undefined, { minimumFractionDigits: 2 })}`
                )}
              </Stat.ValueText>
            </Stat.Root>
          </SimpleGrid>
        </Box>
      </Container>
    </>
  )
}
