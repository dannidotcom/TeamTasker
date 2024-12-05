import {
  AppsOutline,
  GridOutline,
  HomeOutline,
  NewspaperOutline,
  NotificationsOutline,
  PeopleOutline,
  PieChartOutline,
} from "react-ionicons";
import { NavLink } from "react-router-dom";

// Définir le type pour chaque lien de navigation
interface NavLinkType {
  title: string;
  icon: JSX.Element;
  to: string;
}

const Sidebar = (): JSX.Element => {
  const navLinks: NavLinkType[] = [
    { title: "Home", icon: <HomeOutline color="#555" width="22px" height="22px" />, to: "/" },
    { title: "Boards", icon: <AppsOutline color="#555" width="22px" height="22px" />, to: "/boards" },
    { title: "Projects", icon: <GridOutline color="#555" width="22px" height="22px" />, to: "/projects" },
    { title: "Analytics", icon: <PieChartOutline color="#555" width="22px" height="22px" />, to: "/analytics" },
    { title: "Workflows", icon: <PeopleOutline color="#555" width="22px" height="22px" />, to: "/workflows" },
    { title: "Notifications", icon: <NotificationsOutline color="#555" width="22px" height="22px" />, to: "/notifications" },
    { title: "Newsletter", icon: <NewspaperOutline color="#555" width="22px" height="22px" />, to: "/newsletter" },
  ];

  return (
    <div className="fixed left-0 top-0 md:w-[230px] w-[60px] overflow-hidden h-full flex flex-col">
      <div className="w-full flex items-center md:justify-start justify-center md:pl-5 h-[70px] bg-[#fff]">
        <span className="hidden text-2xl font-semibold text-orange-400 md:block">Logo.</span>
        <span className="block text-2xl font-semibold text-orange-400 md:hidden">L.</span>
      </div>
      <div className="w-full h-[calc(100vh-70px)] border-r flex flex-col md:items-start items-center gap-2 border-slate-300 bg-[#fff] py-5 md:px-3 px-3 relative">
        {navLinks.map((link) => {
          return (
            <NavLink
              key={link.title}
              to={link.to}
              className={({ isActive }) =>
                `flex items-center gap-2 w-full rounded-lg px-2 py-3 cursor-pointer ${isActive ? "bg-orange-300" : "bg-transparent"}`
              }
            >
              {link.icon}
              <span className="font-medium text-[15px] md:block hidden">{link.title}</span>
            </NavLink>
          );
        })}
      </div>
    </div>
  );
};

export default Sidebar;
