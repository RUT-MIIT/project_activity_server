import type { FC } from 'react';
import type { ITabsProps } from '../types/types';
import { NavLink } from 'react-router-dom';
import styles from '../styles/tabs.module.scss';

export const Tabs: FC<ITabsProps> = ({ tabs, activeTab, onTabChange }) => {
	return (
		<div className={styles.container}>
			<div className={styles.tabs}>
				{tabs.map((tab) => {
					const isActive =
						activeTab === tab.path ||
						(tab.path && window.location.pathname.endsWith(tab.path));

					// Если таб отключён
					if (tab.disabled) {
						return (
							<div key={tab.path} className={styles.tab_disabled}>
								{tab.label}
							</div>
						);
					}

					// Если есть кастомный обработчик — используем его (не навигация)
					if (onTabChange) {
						return (
							<button
								key={tab.path}
								className={isActive ? styles.tab_active : styles.tab}
								onClick={() => onTabChange(tab.path)}>
								{tab.label}
							</button>
						);
					}

					// Иначе — классическое поведение через NavLink
					return (
						<NavLink
							key={tab.path}
							to={tab.path}
							className={({ isActive }) =>
								isActive ? styles.tab_active : styles.tab
							}>
							{tab.label}
						</NavLink>
					);
				})}
			</div>
		</div>
	);
};
