import { RouteObject } from "react-router";
import Layout from "../layout";
import Boards from "../pages/Boards/Boards";
import Projects from "../pages/Projects/Projects";
import Analytics from "../pages/Analytics/Analytics";
import Workflows from "../pages/Workflows/Workflows";
import Notifications from "../pages/Notifications/Notifications";
import Newsletter from "../pages/Newsletter/Newsletter";
import Home from "../pages/Home/Home";


const routes: RouteObject[] = [
	{
		path: "/",
		element: <Layout />,
		children: [
			{
				children: [
					{
						path: "/",
						element: <Home />
					},
					{
						path: "/boards",
						element: <Boards />
					},
					{
						path: "/projects",
						element: <Projects />,
					},
					{
						path: "/analytics",
						element: <Analytics />,
					},
					{
						path: "/workflows",
						element: <Workflows />,
					},
					{
						path: "/notifications",
						element: <Notifications />,
					},
					{
						path: "/newsletter",
						element: <Newsletter />
					}
				],
			},
		],
	},
];

export default routes;
