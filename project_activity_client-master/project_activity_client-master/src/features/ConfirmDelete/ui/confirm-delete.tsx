import type { FC, FormEvent } from 'react';
import type { IConfirmDelete } from '../types/types';

import { Modal } from '../../../shared/components/Modal/ui/modal';
import { Form } from '../../../shared/components/Form/ui/form';
import { FormButtons } from '../../../shared/components/Form/components';
import { Button } from '../../../shared/components/Button/ui/button';

export const ConfirmDelete: FC<IConfirmDelete> = ({
	isOpen,
	onClose,
	id,
	onSubmit,
}) => {
	const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		onSubmit(id);
	};

	return (
		<Modal
			isOpen={isOpen}
			onClose={onClose}
			modalWidth='small'
			title='Отправить запрос на удаление?'>
			<Form name='form-confirm-delete' onSubmit={handleSubmit}>
				<FormButtons>
					<Button type='submit' text='Удалить' width='full'></Button>
				</FormButtons>
			</Form>
		</Modal>
	);
};
