import type { FC } from 'react';
import type { IWizardProps } from '../types/types';

import styles from '../styles/wizard.module.scss';

export const Wizard: FC<IWizardProps> = ({ id, children }) => {
	return (
		<div data-id={id} className={styles.container}>
			{children}
		</div>
	);
};
