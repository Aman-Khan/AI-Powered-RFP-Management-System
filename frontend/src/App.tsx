import { RouterProvider } from "react-router-dom";
import { router } from "./routes/index";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./lib/queryClient";
import MuiToastProvider from "./components/Toast/MuiToastProvider";

const App = () => (
  <QueryClientProvider client={queryClient}>
    <MuiToastProvider>
      <RouterProvider router={router} />
    </MuiToastProvider>
  </QueryClientProvider>
);

export default App;
