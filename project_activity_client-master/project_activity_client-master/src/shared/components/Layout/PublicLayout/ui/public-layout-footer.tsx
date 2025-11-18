import type { FC } from 'react';

import { currentYear } from '../../../../lib/date';

import styles from '../styles/public-layout.module.scss';

export const PublicLayoutFooter: FC = () => {
	return (
		<footer className={styles.footer}>
			<div className={styles.footer__column}>
				<h4 className={styles.footer__title}>Техническая поддержка:</h4>
				<p className={`${styles.footer__text} ${styles.footer__mail}`}>
					ief07@bk.ru
				</p>
			</div>
			<div className={styles.footer__column}>
				<p className={styles.footer__copy}>
					{currentYear}, Российский университет транспорта
				</p>
			</div>
		</footer>
	);
};
