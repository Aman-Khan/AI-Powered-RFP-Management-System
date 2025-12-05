import { useState } from "react";
import { Outlet, Link as RouterLink, useNavigate } from "react-router-dom";
import {
    AppBar,
    Avatar,
    Badge,
    Box,
    Button,
    Container,
    CssBaseline,
    Divider,
    Drawer,
    IconButton,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    Menu,
    MenuItem,
    Snackbar,
    Toolbar,
    Tooltip,
    Typography,
    useTheme,
    Alert,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import PeopleIcon from "@mui/icons-material/People";
import DescriptionIcon from "@mui/icons-material/Description";
import SendIcon from "@mui/icons-material/Send";
import AssessmentIcon from "@mui/icons-material/Assessment";
import LogoutIcon from "@mui/icons-material/Logout";
import HomeIcon from "@mui/icons-material/Home";
import AddIcon from "@mui/icons-material/Add";
import { NavLink } from "react-router-dom";

const drawerWidth = 260;

export default function AppLayout() {
    const theme = useTheme();
    const navigate = useNavigate();
    const [mobileOpen, setMobileOpen] = useState(false);
    const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
    const [snack, setSnack] = useState<{ open: boolean; message?: string; severity?: "success" | "error" | "info" }>(
        { open: false }
    );

    const handleDrawerToggle = () => setMobileOpen(!mobileOpen);

    const userId = typeof window !== "undefined" ? localStorage.getItem("userId") : null;

    const onLogout = () => {
        localStorage.removeItem("userId");
        setSnack({ open: true, message: "Logged out", severity: "info" });
        navigate("/login", { replace: true });
    };

    const handleAvatarClick = (e: React.MouseEvent<HTMLElement>) => setAnchorEl(e.currentTarget);
    const closeMenu = () => setAnchorEl(null);

    const drawer = (
        <Box sx={{ width: drawerWidth, display: "flex", flexDirection: "column", height: "100%" }}>
            <Box sx={{ px: 3, py: 4 }}>
                <Typography variant="h6" color="primary" fontWeight={700}>
                    RFP Manager
                </Typography>
                <Typography variant="caption" color="text.secondary">
                    Procurement assistant
                </Typography>
            </Box>

            <Divider />

            <List sx={{ flex: 1 }}>

                <ListItem
                    component={NavLink}
                    to="/rfp/create"
                    sx={{
                        borderRadius: 1,
                        mx: 1,
                        "&.active": {
                            backgroundColor: "primary.main",
                            color: "white",
                            "& .MuiListItemIcon-root": { color: "white" }
                        }
                    }}
                >
                    <ListItemIcon><AddIcon /></ListItemIcon>
                    <ListItemText primary="Create RFP" />
                </ListItem>

                <ListItem
                    component={NavLink}
                    to="/rfp/send"
                    sx={{
                        borderRadius: 1,
                        mx: 1,
                        "&.active": {
                            backgroundColor: "primary.main",
                            color: "white",
                            "& .MuiListItemIcon-root": { color: "white" }
                        }
                    }}
                >
                    <ListItemIcon><SendIcon /></ListItemIcon>
                    <ListItemText primary="Send RFPs" />
                </ListItem>

                <ListItem
                    component={NavLink}
                    to="/proposals"
                    sx={{
                        borderRadius: 1,
                        mx: 1,
                        "&.active": {
                            backgroundColor: "primary.main",
                            color: "white",
                            "& .MuiListItemIcon-root": { color: "white" }
                        }
                    }}
                >
                    <ListItemIcon><AssessmentIcon /></ListItemIcon>
                    <ListItemText primary="Proposals" />
                </ListItem>

                <ListItem
                    component={NavLink}
                    to="/vendors"
                    sx={{
                        borderRadius: 1,
                        mx: 1,
                        "&.active": {
                            backgroundColor: "primary.main",
                            color: "white",
                            "& .MuiListItemIcon-root": { color: "white" }
                        }
                    }}
                >
                    <ListItemIcon><PeopleIcon /></ListItemIcon>
                    <ListItemText primary="Vendors" />
                </ListItem>

                <ListItem
                    component={NavLink}
                    to="/users"
                    sx={{
                        borderRadius: 1,
                        mx: 1,
                        "&.active": {
                            backgroundColor: "primary.main",
                            color: "white",
                            "& .MuiListItemIcon-root": { color: "white" }
                        }
                    }}
                >
                    <ListItemIcon><HomeIcon /></ListItemIcon>
                    <ListItemText primary="Users" />
                </ListItem>

                <ListItem
                    component={NavLink}
                    to="/rfp-vendors"
                    sx={{
                        borderRadius: 1,
                        mx: 1,
                        "&.active": {
                            backgroundColor: "primary.main",
                            color: "white",
                            "& .MuiListItemIcon-root": { color: "white" }
                        }
                    }}
                >
                    <ListItemIcon><SendIcon /></ListItemIcon>
                    <ListItemText primary="RFP Requests" />
                </ListItem>


            </List>


            <Divider />

            <Box sx={{ p: 2 }}>
                <Button
                    startIcon={<AddIcon />}
                    variant="contained"
                    color="primary"
                    fullWidth
                    component={RouterLink}
                    to="/rfp/create"
                >
                    New RFP
                </Button>

                <Button
                    startIcon={<LogoutIcon />}
                    variant="outlined"
                    color="inherit"
                    fullWidth
                    sx={{ mt: 1 }}
                    onClick={onLogout}
                >
                    Logout
                </Button>
            </Box>
        </Box>
    );

    return (
        <Box sx={{ display: "flex", minHeight: "100vh" }}>
            <CssBaseline />
            <AppBar position="fixed" color="inherit" elevation={1} sx={{ zIndex: theme.zIndex.drawer + 1 }}>
                <Toolbar sx={{ display: "flex", gap: 2 }}>
                    <IconButton
                        color="inherit"
                        aria-label="open drawer"
                        edge="start"
                        onClick={handleDrawerToggle}
                        sx={{ mr: 1, display: { sm: "none" } }}
                    >
                        <MenuIcon />
                    </IconButton>

                    <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
                        RFP AI — Procurement
                    </Typography>

                    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                        <Tooltip title="Notifications">
                            <IconButton color="inherit" size="large">
                                <Badge badgeContent={2} color="primary">
                                    <SendIcon />
                                </Badge>
                            </IconButton>
                        </Tooltip>

                        <Tooltip title="Account">
                            <IconButton onClick={handleAvatarClick} size="large">
                                <Avatar sx={{ bgcolor: "primary.main" }}>
                                    {userId ? (userId as string).slice(0, 1).toUpperCase() : "U"}
                                </Avatar>
                            </IconButton>
                        </Tooltip>

                        <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={closeMenu}>
                            <MenuItem onClick={() => { closeMenu(); navigate("/users"); }}>Profile</MenuItem>
                            <MenuItem onClick={() => { closeMenu(); onLogout(); }}>Logout</MenuItem>
                        </Menu>
                    </Box>
                </Toolbar>
            </AppBar>

            {/* Drawer for larger screens */}
            <Box component="nav" sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}>
                <Drawer
                    variant="temporary"
                    open={mobileOpen}
                    onClose={handleDrawerToggle}
                    ModalProps={{ keepMounted: true }}
                    sx={{
                        display: { xs: "block", sm: "none" },
                        "& .MuiDrawer-paper": { width: drawerWidth },
                    }}
                >
                    {drawer}
                </Drawer>

                <Drawer
                    variant="permanent"
                    sx={{
                        display: { xs: "none", sm: "block" },
                        "& .MuiDrawer-paper": { width: drawerWidth, top: "64px", height: "calc(100% - 64px)" },
                    }}
                    open
                >
                    {drawer}
                </Drawer>
            </Box>

            {/* Main content */}
            <Box component="main" sx={{ flexGrow: 1, p: { xs: 2, md: 4 }, pt: "88px" }}>
                <Container maxWidth="lg">
                    {/* Breadcrumb / page header could go here */}
                    <Box sx={{ mb: 3 }}>
                        <Typography variant="h5" fontWeight={700}>Dashboard</Typography>
                        <Typography variant="body2" color="text.secondary">Overview & quick actions</Typography>
                    </Box>

                    {/* Page content area */}
                    <Box sx={{ minHeight: "60vh", bgcolor: "background.paper", borderRadius: 2, p: 3, boxShadow: 1 }}>
                        <Outlet />
                    </Box>

                    {/* Footer */}
                    <Box sx={{ mt: 4, textAlign: "center", color: "text.secondary" }}>
                        <Typography variant="caption">© {new Date().getFullYear()} RFP AI — Built with ❤️</Typography>
                    </Box>
                </Container>
            </Box>

            {/* Snackbar (MUI toast) */}
            <Snackbar
                open={snack.open}
                autoHideDuration={3000}
                onClose={() => setSnack({ open: false })}
                anchorOrigin={{ vertical: "top", horizontal: "right" }}
            >
                <Alert onClose={() => setSnack({ open: false })} severity={snack.severity ?? "info"} sx={{ width: "100%" }}>
                    {snack.message}
                </Alert>
            </Snackbar>
        </Box>
    );
}
