import type { FC } from 'react';

import styles from '../styles/preloader.module.scss';

export const Preloader: FC = () => {
	return (
		<figure className={styles.preloader}>
			<i className={styles.circle}></i>
			<figcaption className={styles.caption}>Идёт загрузка...</figcaption>
		</figure>
	);
};
