import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import React from "react";
import ReactDOM from "react-dom/client";
import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
} from "react-router-dom";
import App from "./App";
import "./index.css";
import LandingPage from "./LandingPageNew";
import { ProtectedLayout } from "./layouts/ProtectedLayout";
import Login from "./Login";
import Signup from "./Signup";
import Dashboard from "./pages/Dashboard/Dashboard";

const queryClient = new QueryClient();
// const router = createBrowserRouter([
//   {
//     path: "/",
//     element: <LandingPage />,
//   },
//   {
//     path: "/mytexteditor",
//     element: <App />,
//   },
//   {
//     path: "about",
//     element: <div>About</div>,
//   },
//   {
//     path: "login",
//     element: <Login />,
//   },
// ]);

const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />

      <Route element={<ProtectedLayout />}>
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="editor" element={<App />}>
          <Route path=":docId" element={<App />} />
        </Route>
      </Route>
    </>
  )
);

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <QueryClientProvider client={queryClient}>
    <RouterProvider router={router} />
  </QueryClientProvider>
);
