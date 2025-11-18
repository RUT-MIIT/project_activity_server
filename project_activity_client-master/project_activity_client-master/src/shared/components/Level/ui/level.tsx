import type { FC } from 'react';
import type { ILevelProps } from '../types/types';

import { useState, useEffect, useRef } from 'react';

import { Icon } from '../../Icon/ui/icon';

import styles from '../styles/level.module.scss';

export const Level: FC<ILevelProps> = ({
	title,
	count,
	icons,
	onShow,
	isShow = true,
	children,
}) => {
	const containerRef = useRef<HTMLDivElement>(null);
	const headerRef = useRef<HTMLDivElement>(null);
	const [mainHeight, setMainHeight] = useState<string>('0px');

	useEffect(() => {
		if (containerRef.current && headerRef.current) {
			const containerHeight = containerRef.current.offsetHeight;
			const headerHeight = headerRef.current.offsetHeight;
			setMainHeight(`${containerHeight - headerHeight - 40 - 12}px`);
		}
	}, [isShow]);
	return (
		<>
			{isShow ? (
				<div
					ref={containerRef}
					className={`${styles.container} ${styles.container_show}`}>
					<div ref={headerRef} className={styles.header}>
						<h4 className={styles.title}>{title}</h4>
						<span className={styles.count}>{count}</span>
						<div className={styles.control}>
							{icons?.map((elem, i) => (
								<Icon key={i} icon={elem.icon} onClick={elem.onClick} />
							))}
						</div>
					</div>
					<div className={styles.main} style={{ height: mainHeight }}>
						{children}
					</div>
				</div>
			) : (
				<div
					onClick={onShow}
					className={`${styles.container} ${styles.container_hide}`}>
					<h4 className={`${styles.title} ${styles.title_hide}`}>{title}</h4>
				</div>
			)}
		</>
	);
};
