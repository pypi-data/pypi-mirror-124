/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { ServerConnection } from '@jupyterlab/services';

import * as React from 'react';
import { Global } from '../Global';

import { DeployPage } from './DeployPage';
import { MonitorPage } from './MonitorPage';

import {
	Tabs,
	Tab,
	Badge,
	SvgIcon,
	Theme,
	withTheme,
	withStyles,
} from '@material-ui/core';

import { MachinesPage } from './MachinesPage';
import { ShadowedDivider } from '../core';

import { SnackbarKey, withSnackbar, WithSnackbarProps } from 'notistack';
import { Snackbar } from '../models/Snackbar';
import { UserDialog } from './UserDialog';
import moment from 'moment';
import { Machine } from '../models/machine/Machine';
import { BillingType } from '../models/User';

import LocalShippingIcon from '@material-ui/icons/LocalShipping';
import { SubmitPage } from './SubmitPage';
import { PackageState } from '../models/Package';

const WarningBadge = withStyles({ badge: { fontWeight: 'bold' }, colorPrimary: { backgroundColor: '#ffba7d' } })(Badge)

// Properties from parent
interface IProps extends WithSnackbarProps {
	theme: Theme
}

enum Page {
	SUBMIT = 0,
	DEPLOY = 1,
	MONITOR = 2,
	MACHINES = 3,
}

// Properties for this component
interface IState {
	page: Page;
	deployDisabled: boolean;
    cost: number,
    balance: number,
	machines: Machine[],
	rate: number,
}

class Pilot extends React.Component<IProps, IState> {
	_isMounted = false;
	private polling = false;

	openUserDialogTo: (page: number) => Promise<void> = () => new Promise<void>(resolve => resolve()) // This is somewhat spaghetti code-y, maybe think about revising

	constructor(props: IProps) {
		super(props);
		this.state = {
			page: Global.user.lastPage,
			deployDisabled: false,
            cost: Global.lastCreditsCost,
            balance: Global.lastCreditsBalance,
			machines: [],
			rate: 0,
		}
	}

	private handleTabChange = (event: React.ChangeEvent<{}>, newValue: Page) => {
		if (newValue == Page.MACHINES) this.updateMachines(false)
		this.safeSetState({ page: newValue });
		Global.user.lastPage = newValue;
	}

    private previousCostUpdate: any
    private async receiveCostUpdate() {
		const settings = ServerConnection.makeSettings();
        const url = settings.baseUrl + "optumi/get-total-billing";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				startTime: new Date(0).toISOString(),
				endTime: new Date().toISOString(),
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			if (this.polling) {
				// If we are polling, send a new request in 2 seconds
                if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
				setTimeout(() => this.receiveCostUpdate(), 2000);
			}
            Global.handleResponse(response);
			return response.json();
		}).then((body: any) => {
			if (body) {
				if (JSON.stringify(body) !== JSON.stringify(this.previousCostUpdate)) {
                    this.safeSetState({ balance: body.balance, cost: body.total });
                    this.previousCostUpdate = body
                }
			}
		});
	}

    private previousMachines: any
    private updateMachines = (scheduleNew: boolean = true) => {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/get-machines";
		const init = {
			method: 'GET',
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
            if (this.polling && scheduleNew) {
                // If we are polling, send a new request in 2 seconds
                if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
                setTimeout(() => this.updateMachines(), 2000);
            }
            Global.handleResponse(response);
			return response.json();
		}).then((body: any) => {
            var machines: Machine[] = []
            for (var i = 0; i < body.machines.length; i++) {
                machines.push(Object.setPrototypeOf(body.machines[i], Machine.prototype));
            }
            if (JSON.stringify(body) !== JSON.stringify(this.previousMachines)) {
				var rate = 0;
				for (let machine of machines) {
					if (machine.getStateMessage() != 'Releasing') rate += +(machine.rate.toFixed(2))
				}
                this.safeSetState({ machines: machines, rate: rate });
                this.previousMachines = body
            }
		}, () => {
			if (this.polling && scheduleNew) setTimeout(() => this.updateMachines(), 2000);
		});
    }

	private getPackageBadge = () => {
		if (Global.metadata) {
			const pack = Global.metadata.getPackage(true);
			if (pack == null) {
				return 0;
			} else if (pack.packageState == PackageState.SHIPPED) {
				return '!';
			} else {
				return 0;
			}
		} else {
			return 0;
		}
    }

	// The contents of the component
	public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
		return (
			<>
				<div style={{paddingBottom: "5px", textAlign: 'center', verticalAlign: 'middle'}}>
                    <div style={{display: 'inline-flex', width: '100%'}}>
						<a href='https://www.optumi.com' target='_blank'>
							<div className='jp-optumi-logo' />
						</a>
						<UserDialog style={{margin: 'auto 6px auto auto'}} getOpenTo={(openTo: (page: number) => Promise<void>) => {
							this.openUserDialogTo = openTo
							this.forceUpdate()
						}} />
					</div>
					<Tabs
						value={this.state.page}
						onChange={this.handleTabChange}
						variant="fullWidth"
						indicatorColor="primary"
						textColor="primary"
						style={{margin: '0px 6px'}}
					>
						<Tab
							icon={
								<LocalShippingIcon style={{width: '28px', height: '28px'}} />
							} /*label="SUBMIT"*/ style={{minWidth: "72px"}} />
						<Tab
							icon={
								<Badge
									badgeContent={this.getPackageBadge()}
									anchorOrigin={{ vertical: 'top', horizontal: 'left',}}
									color={"primary"}>
									<SvgIcon viewBox="0, 0, 400,446" style={{width: '28px', height: '28px'}}>
										<path d="M348.000 58.232 C 324.618 61.984,306.000 66.674,306.000 68.813 C 306.000 71.851,369.545 135.122,371.067 133.599 C 372.905 131.761,382.000 74.336,382.000 64.567 L 382.000 56.000 370.500 56.234 C 364.175 56.362,354.050 57.262,348.000 58.232 M261.029 86.235 C 214.374 111.539,184.827 137.455,151.438 182.354 C 131.859 208.683,134.247 207.280,105.973 209.077 C 77.646 210.877,78.107 210.586,46.111 246.944 C 14.709 282.628,13.657 285.006,24.595 295.608 C 33.914 304.640,38.535 303.841,62.774 289.000 C 74.453 281.850,85.356 276.000,87.004 276.000 C 90.397 276.000,91.021 279.133,88.000 281.000 C 80.966 285.347,86.211 293.260,115.524 322.525 C 145.290 352.241,154.153 357.842,159.000 350.000 C 161.093 346.613,163.948 347.791,162.638 351.500 C 161.957 353.425,155.685 364.580,148.700 376.288 C 133.629 401.551,133.207 405.011,144.006 414.767 C 155.049 424.744,153.659 425.401,190.701 392.696 C 227.821 359.922,227.156 360.976,229.004 332.000 C 230.748 304.673,229.916 306.203,252.454 288.864 C 308.578 245.687,341.585 206.858,361.005 161.165 C 368.325 143.941,367.373 141.488,347.134 125.396 C 330.680 112.314,319.724 100.874,305.577 82.000 C 295.803 68.959,292.260 69.296,261.029 86.235 M281.518 145.989 C 295.397 154.451,299.651 169.944,291.460 182.204 C 279.075 200.744,254.612 198.973,245.060 178.845 C 234.650 156.906,260.788 133.350,281.518 145.989 M65.116 318.984 C 41.834 327.278,33.655 343.820,22.828 404.507 C 19.046 425.702,19.740 429.180,26.337 422.099 C 32.573 415.406,48.022 408.969,72.496 402.867 C 109.336 393.683,120.097 382.787,119.904 354.869 L 119.808 341.000 116.404 347.823 C 111.679 357.294,105.398 361.342,88.000 366.125 C 79.750 368.394,70.975 371.564,68.500 373.171 C 63.012 376.734,63.005 376.424,68.070 354.701 C 73.737 330.396,81.234 320.000,93.094 320.000 C 94.692 320.000,96.000 319.100,96.000 318.000 C 96.000 315.041,74.239 315.734,65.116 318.984 " />
									</SvgIcon>
								</Badge>
							} /*label="DEPLOY"*/ style={{minWidth: "72px"}} />
						<Tab 
							icon={
								<Badge
									badgeContent={Global.user.appTracker.getDisplayNum()}
									anchorOrigin={{ vertical: 'top', horizontal: 'left',}}
									color={"primary"}>
										<SvgIcon viewBox="0, 0, 400,400" style={{width: '28px', height: '28px'}}>
											<path d="M184.000 75.671 C 157.886 84.352,136.646 102.091,124.338 125.500 L 117.765 138.000 105.383 138.035 C 90.924 138.075,71.538 141.909,56.000 147.801 C -14.626 174.580,-18.484 281.128,49.988 313.831 L 65.000 321.000 203.705 321.553 L 342.409 322.106 353.376 317.085 C 385.732 302.272,399.199 277.664,397.610 236.256 C 396.006 194.437,366.443 166.000,324.574 166.000 C 319.271 166.000,315.638 165.024,315.269 163.500 C 304.910 120.762,285.610 93.164,256.447 79.388 C 239.169 71.226,202.961 69.368,184.000 75.671 M244.970 147.777 C 301.927 179.760,259.786 271.237,199.913 245.586 L 192.826 242.549 169.913 267.273 C 142.622 296.721,133.842 300.366,127.894 284.720 C 125.394 278.145,125.295 278.289,151.476 250.369 L 173.952 226.400 169.629 216.700 C 148.789 169.946,200.388 122.743,244.970 147.777 M206.094 158.498 C 190.267 163.800,177.795 184.895,181.098 200.776 C 190.562 246.287,256.850 241.187,256.856 194.948 C 256.859 168.669,231.052 150.138,206.094 158.498 " />
										</SvgIcon>
								</Badge>
							} /*label="MONITOR"*/ style={{minWidth: "72px"}} />
						<Tab 
							icon={
								(() => {
									const dur = moment.duration(-this.state.balance / this.state.rate, 'hours');
									if (Global.user.billingType == BillingType.CREDIT_BUCKET && dur.asHours() < 25) {
										return (<WarningBadge
											badgeContent='!'
											anchorOrigin={{ vertical: 'top', horizontal: 'left',}}
											color={dur.asHours() <= 2 ? "error" : "primary"}>
												<SvgIcon viewBox="0, 0, 400,200" style={{width: '28px', height: '28px'}}>
													<path d="M0.000 40.000 L 0.000 80.000 200.000 80.000 L 400.000 80.000 400.000 40.000 L 400.000 0.000 200.000 0.000 L 0.000 0.000 0.000 40.000 M80.000 40.000 L 80.000 60.000 60.000 60.000 L 40.000 60.000 40.000 40.000 L 40.000 20.000 60.000 20.000 L 80.000 20.000 80.000 40.000 M0.000 160.000 L 0.000 200.000 200.000 200.000 L 400.000 200.000 400.000 160.000 L 400.000 120.000 200.000 120.000 L 0.000 120.000 0.000 160.000 M80.000 160.000 L 80.000 180.000 60.000 180.000 L 40.000 180.000 40.000 160.000 L 40.000 140.000 60.000 140.000 L 80.000 140.000 80.000 160.000 " />
												</SvgIcon>
										</WarningBadge>)
									}
									return (
										<SvgIcon viewBox="0, 0, 400,200" style={{width: '28px', height: '28px'}}>
											<path d="M0.000 40.000 L 0.000 80.000 200.000 80.000 L 400.000 80.000 400.000 40.000 L 400.000 0.000 200.000 0.000 L 0.000 0.000 0.000 40.000 M80.000 40.000 L 80.000 60.000 60.000 60.000 L 40.000 60.000 40.000 40.000 L 40.000 20.000 60.000 20.000 L 80.000 20.000 80.000 40.000 M0.000 160.000 L 0.000 200.000 200.000 200.000 L 400.000 200.000 400.000 160.000 L 400.000 120.000 200.000 120.000 L 0.000 120.000 0.000 160.000 M80.000 160.000 L 80.000 180.000 60.000 180.000 L 40.000 180.000 40.000 160.000 L 40.000 140.000 60.000 140.000 L 80.000 140.000 80.000 160.000 " />
										</SvgIcon>
									)
								})()
							} /*label="MACHINES"*/ style={{minWidth: "72px"}} />
					</Tabs>
				</div>
				<ShadowedDivider />
				{this.state.page == Page.SUBMIT ? (
					<SubmitPage style={{flexGrow: 1}} openDeployPage={() => this.safeSetState({ page: Page.DEPLOY })}/>
				) : this.state.page == Page.DEPLOY ? (
					<DeployPage style={{flexGrow: 1}} openUserDialogTo={this.openUserDialogTo} />
				) : this.state.page == Page.MONITOR ? (
					<MonitorPage style={{flexGrow: 1}} openUserDialogTo={this.openUserDialogTo}/>
				) : this.state.page == Page.MACHINES ? (
					<MachinesPage style={{flexGrow: 1}} rate={this.state.rate} cost={this.state.cost} balance={this.state.balance} machines={this.state.machines}/>
				) : (
					<></>
				)}
			</>
		);
	}

    private handleSnackbarEnqueue = (sender: Global, snackbar: Snackbar) => this.props.enqueueSnackbar(snackbar.message, snackbar.options)
    private handleSnackbarClose = (sender: Global, key: SnackbarKey) => this.props.closeSnackbar(key)
    private handleAppsChange = () => this.forceUpdate()
    private handlePackageChange = () => this.forceUpdate()
	private handleChange = () => this.forceUpdate();

	private handleForcePackageIntoView = () => {
		Global.lastForceCompleted = false;
		this.setState({ page: Page.DEPLOY })
	}
	private handleJobLaunched = (): any => void 0 /*this.safeSetState({ page: Page.Monitor })*/

	// Will be called automatically when the component is mounted
	public componentDidMount = () => {
		this._isMounted = true;
		this.polling = true;
        this.receiveCostUpdate();
		this.updateMachines();
		Global.labShell.currentChanged.connect(this.handleChange);
		Global.tracker.currentChanged.connect(this.handleChange);
        Global.tracker.selectionChanged.connect(this.handleChange);
        Global.user.appTracker.appsChanged.connect(this.handleAppsChange);
		Global.snackbarEnqueue.connect(this.handleSnackbarEnqueue);
		Global.snackbarClose.connect(this.handleSnackbarClose);
		Global.jobLaunched.connect(this.handleJobLaunched);
		Global.metadata.getPackageChanged().connect(this.handlePackageChange)
		Global.forcePackageIntoView.connect(this.handleForcePackageIntoView);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
		Global.labShell.currentChanged.disconnect(this.handleChange);
		Global.tracker.currentChanged.disconnect(this.handleChange);
        Global.tracker.selectionChanged.disconnect(this.handleChange);
        Global.user.appTracker.appsChanged.disconnect(this.handleAppsChange);
		Global.snackbarEnqueue.disconnect(this.handleSnackbarEnqueue);
		Global.snackbarClose.disconnect(this.handleSnackbarClose);
		Global.jobLaunched.disconnect(this.handleJobLaunched);
		Global.metadata.getPackageChanged().disconnect(this.handlePackageChange);
		Global.forcePackageIntoView.disconnect(this.handleForcePackageIntoView);
		Global.lastMachineRate = this.state.cost;
        Global.lastCreditsCost = this.state.cost;
        Global.lastCreditsBalance = this.state.balance;
        this.polling = false;
		this._isMounted = false;
	}

	private safeSetState = (map: any) => {
		if (this._isMounted) {
			let update = false
			try {
				for (const key of Object.keys(map)) {
					if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
						update = true
						break
					}
				}
			} catch (error) {
				update = true
			}
			if (update) {
				if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
				this.setState(map)
			} else {
				if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
			}
		}
	}

	public shouldComponentUpdate = (nextProps: IProps, nextState: IState): boolean => {
        try {
            if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
            if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
            if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
            return false;
        } catch (error) {
            return true;
        }
    }
}


const SnackbarPilot = withSnackbar(Pilot);
const ThemedPilot = withTheme(SnackbarPilot);
export { ThemedPilot as Pilot }
