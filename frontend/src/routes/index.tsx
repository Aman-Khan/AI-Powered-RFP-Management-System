import { createBrowserRouter } from "react-router-dom";
import CreateRFP from "../pages/CreateRFP/CreateRFP";
// import Vendors from "../pages/Vendors/Vendors";
// import Proposals from "../pages/Proposals/Proposals";
// import Compare from "../pages/Compare/Compare";

export const router = createBrowserRouter([
  { path: "/", element: <CreateRFP /> },
//   { path: "/vendors", element: <Vendors /> },
//   { path: "/proposals", element: <Proposals /> },
//   { path: "/compare/:rfpId", element: <Compare /> },
]);
