import { createBrowserRouter } from "react-router-dom";
import AppLayout from "../components/Layout/AppLayout";
import ProtectedRoute from "../components/Auth/ProtectedRoute";

// Pages
import Login from "../pages/User/Login";
import UserList from "../pages/User/UserList";
import CreateUser from "../pages/User/CreateUser";
import EditUser from "../pages/User/EditUser";

import CreateRFP from "../pages/RFP/CreateRFP";
import SendRFP from "../pages/RFP/SendRFP";
import VendorList from "../pages/Vendors/VendorList";
import RfpSendViewPage from "../pages/RFP/RfpSendView";
import RfpSendToVendors from "../pages/RFP/RfpSendToVendors";
// import RfpVendorList from "../pages/RFP/RfpVendorList";
// import RfpVendorDetail from "../pages/RFP/RfpVendorDetail";
// import RfpVendorTree from "../pages/RFP/RfpVendorTree";
import RfpVendorTable from "../pages/RFPVendor/RfpVendorTable";
import ProposalTable from "../pages/Proposal/ProposalTable";

export const router = createBrowserRouter([
  { path: "/login", element: <Login /> },

  {
    path: "/",
    element: <ProtectedRoute />,
    children: [
      {
        path: "",
        element: <AppLayout />,
        children: [
          // Users
          { path: "users", element: <UserList /> },
          { path: "users/create", element: <CreateUser /> },
          { path: "users/edit/:id", element: <EditUser /> },

          // RFP
          { path: "rfp/create", element: <CreateRFP /> },
          { path: "rfp/send", element: <SendRFP /> },
          // { path: "rfp/vendors", element: <RfpVendorTree /> },
          { path: "rfp-vendors", element: <RfpVendorTable /> },
          // { path: "rfp-vendors", element: <RfpVendorList /> },
          // { path: "rfp-vendors/:id", element: <RfpVendorDetail /> },
          // NEW SEND VIEW PAGE
          { path: "rfp/send/:id", element: <RfpSendViewPage /> },
          { path: "rfp/send/:id/vendors", element: <RfpSendToVendors /> },

          // Vendors
          { path: "vendors", element: <VendorList /> },
          // Proposals (Coming Later)
          { path: "proposals", element: <ProposalTable /> },
        ],
      },
    ],
  },
]);
