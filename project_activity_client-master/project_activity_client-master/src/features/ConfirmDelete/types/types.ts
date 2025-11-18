export interface IConfirmDelete {
	isOpen: boolean;
	onClose: () => void;
	id: number;
	onSubmit: (id: number) => void;
}
