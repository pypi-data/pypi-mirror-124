/* This file was generated from the org-mode file.
   To generate it, open templator_hdf5.org file in Emacs and execute
   M-x org-babel-tangle
*/

#include "trexio_hdf5.h"
#define METADATA_GROUP_NAME          "metadata"
#define ELECTRON_GROUP_NAME          "electron"
#define NUCLEUS_GROUP_NAME          "nucleus"
#define ECP_GROUP_NAME          "ecp"
#define BASIS_GROUP_NAME          "basis"
#define AO_GROUP_NAME          "ao"
#define AO_1E_INT_GROUP_NAME          "ao_1e_int"
#define AO_2E_INT_GROUP_NAME          "ao_2e_int"
#define MO_GROUP_NAME          "mo"
#define MO_1E_INT_GROUP_NAME          "mo_1e_int"
#define MO_2E_INT_GROUP_NAME          "mo_2e_int"
#define METADATA_CODE_NUM_NAME            "metadata_code_num"
#define METADATA_AUTHOR_NUM_NAME            "metadata_author_num"
#define ELECTRON_UP_NUM_NAME            "electron_up_num"
#define ELECTRON_DN_NUM_NAME            "electron_dn_num"
#define NUCLEUS_NUM_NAME            "nucleus_num"
#define ECP_NUM_NAME            "ecp_num"
#define BASIS_PRIM_NUM_NAME            "basis_prim_num"
#define BASIS_SHELL_NUM_NAME            "basis_shell_num"
#define AO_CARTESIAN_NAME            "ao_cartesian"
#define AO_NUM_NAME            "ao_num"
#define MO_NUM_NAME            "mo_num"
#define NUCLEUS_CHARGE_NAME           "nucleus_charge"
#define NUCLEUS_COORD_NAME           "nucleus_coord"
#define ECP_MAX_ANG_MOM_PLUS_1_NAME           "ecp_max_ang_mom_plus_1"
#define ECP_Z_CORE_NAME           "ecp_z_core"
#define ECP_ANG_MOM_NAME           "ecp_ang_mom"
#define ECP_NUCLEUS_INDEX_NAME           "ecp_nucleus_index"
#define ECP_EXPONENT_NAME           "ecp_exponent"
#define ECP_COEFFICIENT_NAME           "ecp_coefficient"
#define ECP_POWER_NAME           "ecp_power"
#define BASIS_NUCLEUS_INDEX_NAME           "basis_nucleus_index"
#define BASIS_SHELL_ANG_MOM_NAME           "basis_shell_ang_mom"
#define BASIS_SHELL_FACTOR_NAME           "basis_shell_factor"
#define BASIS_SHELL_INDEX_NAME           "basis_shell_index"
#define BASIS_EXPONENT_NAME           "basis_exponent"
#define BASIS_COEFFICIENT_NAME           "basis_coefficient"
#define BASIS_PRIM_FACTOR_NAME           "basis_prim_factor"
#define AO_SHELL_NAME           "ao_shell"
#define AO_NORMALIZATION_NAME           "ao_normalization"
#define AO_1E_INT_OVERLAP_NAME           "ao_1e_int_overlap"
#define AO_1E_INT_KINETIC_NAME           "ao_1e_int_kinetic"
#define AO_1E_INT_POTENTIAL_N_E_NAME           "ao_1e_int_potential_n_e"
#define AO_1E_INT_ECP_LOCAL_NAME           "ao_1e_int_ecp_local"
#define AO_1E_INT_ECP_NON_LOCAL_NAME           "ao_1e_int_ecp_non_local"
#define AO_1E_INT_CORE_HAMILTONIAN_NAME           "ao_1e_int_core_hamiltonian"
#define AO_2E_INT_ERI_NAME           "ao_2e_int_eri"
#define AO_2E_INT_ERI_LR_NAME           "ao_2e_int_eri_lr"
#define MO_COEFFICIENT_NAME           "mo_coefficient"
#define MO_OCCUPATION_NAME           "mo_occupation"
#define MO_1E_INT_OVERLAP_NAME           "mo_1e_int_overlap"
#define MO_1E_INT_KINETIC_NAME           "mo_1e_int_kinetic"
#define MO_1E_INT_POTENTIAL_N_E_NAME           "mo_1e_int_potential_n_e"
#define MO_1E_INT_ECP_LOCAL_NAME           "mo_1e_int_ecp_local"
#define MO_1E_INT_ECP_NON_LOCAL_NAME           "mo_1e_int_ecp_non_local"
#define MO_1E_INT_CORE_HAMILTONIAN_NAME           "mo_1e_int_core_hamiltonian"
#define MO_2E_INT_ERI_NAME           "mo_2e_int_eri"
#define MO_2E_INT_ERI_LR_NAME           "mo_2e_int_eri_lr"
#define METADATA_CODE_NAME           "metadata_code"
#define METADATA_AUTHOR_NAME           "metadata_author"
#define NUCLEUS_LABEL_NAME           "nucleus_label"
#define MO_CLASS_NAME           "mo_class"
#define MO_SYMMETRY_NAME           "mo_symmetry"
#define METADATA_PACKAGE_VERSION_NAME            "metadata_package_version"
#define METADATA_DESCRIPTION_NAME            "metadata_description"
#define NUCLEUS_POINT_GROUP_NAME            "nucleus_point_group"
#define BASIS_TYPE_NAME            "basis_type"
#define MO_TYPE_NAME            "mo_type"

trexio_exit_code
trexio_hdf5_init (trexio_t* const file)
{

  trexio_hdf5_t* const f = (trexio_hdf5_t*) file;

  /* If file doesn't exist, create it */
  int f_exists = 0;
  struct stat st;

  if (stat(file->file_name, &st) == 0) f_exists = 1;

  if (f_exists == 1) {

    switch (file->mode) {
    case 'r':
      // reading the existing file -> open as RDONLY
      f->file_id = H5Fopen(file->file_name, H5F_ACC_RDONLY, H5P_DEFAULT);
      break;
    case 'w':
      // writing the existing file -> open as RDWRITE
      f->file_id = H5Fopen(file->file_name, H5F_ACC_RDWR, H5P_DEFAULT);
      break;
    }

  } else {

    switch (file->mode) {
    case 'r':
      // reading non-existing file -> error
      return TREXIO_FAILURE;
    case 'w':
      // writing non-existing file -> create it
      f->file_id = H5Fcreate(file->file_name, H5F_ACC_EXCL, H5P_DEFAULT, H5P_DEFAULT);
      break;
    }

  }

  /* Create or open groups in the hdf5 file assuming that they exist if file exists */
  switch (file->mode) {
    case 'r':
      f->metadata_group = H5Gopen(f->file_id, METADATA_GROUP_NAME, H5P_DEFAULT);
      f->electron_group = H5Gopen(f->file_id, ELECTRON_GROUP_NAME, H5P_DEFAULT);
      f->nucleus_group = H5Gopen(f->file_id, NUCLEUS_GROUP_NAME, H5P_DEFAULT);
      f->ecp_group = H5Gopen(f->file_id, ECP_GROUP_NAME, H5P_DEFAULT);
      f->basis_group = H5Gopen(f->file_id, BASIS_GROUP_NAME, H5P_DEFAULT);
      f->ao_group = H5Gopen(f->file_id, AO_GROUP_NAME, H5P_DEFAULT);
      f->ao_1e_int_group = H5Gopen(f->file_id, AO_1E_INT_GROUP_NAME, H5P_DEFAULT);
      f->ao_2e_int_group = H5Gopen(f->file_id, AO_2E_INT_GROUP_NAME, H5P_DEFAULT);
      f->mo_group = H5Gopen(f->file_id, MO_GROUP_NAME, H5P_DEFAULT);
      f->mo_1e_int_group = H5Gopen(f->file_id, MO_1E_INT_GROUP_NAME, H5P_DEFAULT);
      f->mo_2e_int_group = H5Gopen(f->file_id, MO_2E_INT_GROUP_NAME, H5P_DEFAULT);
      break;
    case 'w':
      if (f_exists == 1) {
        f->metadata_group = H5Gopen(f->file_id, METADATA_GROUP_NAME, H5P_DEFAULT);
        f->electron_group = H5Gopen(f->file_id, ELECTRON_GROUP_NAME, H5P_DEFAULT);
        f->nucleus_group = H5Gopen(f->file_id, NUCLEUS_GROUP_NAME, H5P_DEFAULT);
        f->ecp_group = H5Gopen(f->file_id, ECP_GROUP_NAME, H5P_DEFAULT);
        f->basis_group = H5Gopen(f->file_id, BASIS_GROUP_NAME, H5P_DEFAULT);
        f->ao_group = H5Gopen(f->file_id, AO_GROUP_NAME, H5P_DEFAULT);
        f->ao_1e_int_group = H5Gopen(f->file_id, AO_1E_INT_GROUP_NAME, H5P_DEFAULT);
        f->ao_2e_int_group = H5Gopen(f->file_id, AO_2E_INT_GROUP_NAME, H5P_DEFAULT);
        f->mo_group = H5Gopen(f->file_id, MO_GROUP_NAME, H5P_DEFAULT);
        f->mo_1e_int_group = H5Gopen(f->file_id, MO_1E_INT_GROUP_NAME, H5P_DEFAULT);
        f->mo_2e_int_group = H5Gopen(f->file_id, MO_2E_INT_GROUP_NAME, H5P_DEFAULT);
      } else {
        f->metadata_group = H5Gcreate(f->file_id, METADATA_GROUP_NAME, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
        f->electron_group = H5Gcreate(f->file_id, ELECTRON_GROUP_NAME, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
        f->nucleus_group = H5Gcreate(f->file_id, NUCLEUS_GROUP_NAME, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
        f->ecp_group = H5Gcreate(f->file_id, ECP_GROUP_NAME, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
        f->basis_group = H5Gcreate(f->file_id, BASIS_GROUP_NAME, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
        f->ao_group = H5Gcreate(f->file_id, AO_GROUP_NAME, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
        f->ao_1e_int_group = H5Gcreate(f->file_id, AO_1E_INT_GROUP_NAME, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
        f->ao_2e_int_group = H5Gcreate(f->file_id, AO_2E_INT_GROUP_NAME, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
        f->mo_group = H5Gcreate(f->file_id, MO_GROUP_NAME, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
        f->mo_1e_int_group = H5Gcreate(f->file_id, MO_1E_INT_GROUP_NAME, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
        f->mo_2e_int_group = H5Gcreate(f->file_id, MO_2E_INT_GROUP_NAME, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
      }
      break;
  }
  if (f->metadata_group <= 0L) return TREXIO_INVALID_ID;
  if (f->electron_group <= 0L) return TREXIO_INVALID_ID;
  if (f->nucleus_group <= 0L) return TREXIO_INVALID_ID;
  if (f->ecp_group <= 0L) return TREXIO_INVALID_ID;
  if (f->basis_group <= 0L) return TREXIO_INVALID_ID;
  if (f->ao_group <= 0L) return TREXIO_INVALID_ID;
  if (f->ao_1e_int_group <= 0L) return TREXIO_INVALID_ID;
  if (f->ao_2e_int_group <= 0L) return TREXIO_INVALID_ID;
  if (f->mo_group <= 0L) return TREXIO_INVALID_ID;
  if (f->mo_1e_int_group <= 0L) return TREXIO_INVALID_ID;
  if (f->mo_2e_int_group <= 0L) return TREXIO_INVALID_ID;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_deinit (trexio_t* const file)
{

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  H5Gclose(f->metadata_group);
  H5Gclose(f->electron_group);
  H5Gclose(f->nucleus_group);
  H5Gclose(f->ecp_group);
  H5Gclose(f->basis_group);
  H5Gclose(f->ao_group);
  H5Gclose(f->ao_1e_int_group);
  H5Gclose(f->ao_2e_int_group);
  H5Gclose(f->mo_group);
  H5Gclose(f->mo_1e_int_group);
  H5Gclose(f->mo_2e_int_group);
  f->metadata_group = 0;
  f->electron_group = 0;
  f->nucleus_group = 0;
  f->ecp_group = 0;
  f->basis_group = 0;
  f->ao_group = 0;
  f->ao_1e_int_group = 0;
  f->ao_2e_int_group = 0;
  f->mo_group = 0;
  f->mo_1e_int_group = 0;
  f->mo_2e_int_group = 0;

  H5Fclose(f->file_id);
  f->file_id = 0;

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_has_metadata_code_num (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  htri_t status = H5Aexists(f->metadata_group, METADATA_CODE_NUM_NAME);
  /* H5Aexists returns positive value if attribute exists, 0 if does not, negative if error */
  if (status > 0){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_metadata_author_num (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  htri_t status = H5Aexists(f->metadata_group, METADATA_AUTHOR_NUM_NAME);
  /* H5Aexists returns positive value if attribute exists, 0 if does not, negative if error */
  if (status > 0){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_electron_up_num (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  htri_t status = H5Aexists(f->electron_group, ELECTRON_UP_NUM_NAME);
  /* H5Aexists returns positive value if attribute exists, 0 if does not, negative if error */
  if (status > 0){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_electron_dn_num (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  htri_t status = H5Aexists(f->electron_group, ELECTRON_DN_NUM_NAME);
  /* H5Aexists returns positive value if attribute exists, 0 if does not, negative if error */
  if (status > 0){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_nucleus_num (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  htri_t status = H5Aexists(f->nucleus_group, NUCLEUS_NUM_NAME);
  /* H5Aexists returns positive value if attribute exists, 0 if does not, negative if error */
  if (status > 0){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_ecp_num (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  htri_t status = H5Aexists(f->ecp_group, ECP_NUM_NAME);
  /* H5Aexists returns positive value if attribute exists, 0 if does not, negative if error */
  if (status > 0){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_basis_prim_num (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  htri_t status = H5Aexists(f->basis_group, BASIS_PRIM_NUM_NAME);
  /* H5Aexists returns positive value if attribute exists, 0 if does not, negative if error */
  if (status > 0){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_basis_shell_num (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  htri_t status = H5Aexists(f->basis_group, BASIS_SHELL_NUM_NAME);
  /* H5Aexists returns positive value if attribute exists, 0 if does not, negative if error */
  if (status > 0){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_ao_cartesian (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  htri_t status = H5Aexists(f->ao_group, AO_CARTESIAN_NAME);
  /* H5Aexists returns positive value if attribute exists, 0 if does not, negative if error */
  if (status > 0){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_ao_num (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  htri_t status = H5Aexists(f->ao_group, AO_NUM_NAME);
  /* H5Aexists returns positive value if attribute exists, 0 if does not, negative if error */
  if (status > 0){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_mo_num (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  htri_t status = H5Aexists(f->mo_group, MO_NUM_NAME);
  /* H5Aexists returns positive value if attribute exists, 0 if does not, negative if error */
  if (status > 0){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_metadata_package_version (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  htri_t status = H5Aexists(f->metadata_group, METADATA_PACKAGE_VERSION_NAME);
  /* H5Aexists returns positive value if attribute exists, 0 if does not, negative if error */
  if (status > 0){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_metadata_description (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  htri_t status = H5Aexists(f->metadata_group, METADATA_DESCRIPTION_NAME);
  /* H5Aexists returns positive value if attribute exists, 0 if does not, negative if error */
  if (status > 0){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_nucleus_point_group (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  htri_t status = H5Aexists(f->nucleus_group, NUCLEUS_POINT_GROUP_NAME);
  /* H5Aexists returns positive value if attribute exists, 0 if does not, negative if error */
  if (status > 0){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_basis_type (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  htri_t status = H5Aexists(f->basis_group, BASIS_TYPE_NAME);
  /* H5Aexists returns positive value if attribute exists, 0 if does not, negative if error */
  if (status > 0){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_mo_type (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  htri_t status = H5Aexists(f->mo_group, MO_TYPE_NAME);
  /* H5Aexists returns positive value if attribute exists, 0 if does not, negative if error */
  if (status > 0){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_nucleus_charge (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->nucleus_group, NUCLEUS_CHARGE_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_nucleus_coord (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->nucleus_group, NUCLEUS_COORD_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_ecp_max_ang_mom_plus_1 (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->ecp_group, ECP_MAX_ANG_MOM_PLUS_1_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_ecp_z_core (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->ecp_group, ECP_Z_CORE_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_ecp_ang_mom (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->ecp_group, ECP_ANG_MOM_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_ecp_nucleus_index (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->ecp_group, ECP_NUCLEUS_INDEX_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_ecp_exponent (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->ecp_group, ECP_EXPONENT_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_ecp_coefficient (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->ecp_group, ECP_COEFFICIENT_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_ecp_power (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->ecp_group, ECP_POWER_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_basis_nucleus_index (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->basis_group, BASIS_NUCLEUS_INDEX_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_basis_shell_ang_mom (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->basis_group, BASIS_SHELL_ANG_MOM_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_basis_shell_factor (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->basis_group, BASIS_SHELL_FACTOR_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_basis_shell_index (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->basis_group, BASIS_SHELL_INDEX_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_basis_exponent (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->basis_group, BASIS_EXPONENT_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_basis_coefficient (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->basis_group, BASIS_COEFFICIENT_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_basis_prim_factor (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->basis_group, BASIS_PRIM_FACTOR_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_ao_shell (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->ao_group, AO_SHELL_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_ao_normalization (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->ao_group, AO_NORMALIZATION_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_ao_1e_int_overlap (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->ao_1e_int_group, AO_1E_INT_OVERLAP_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_ao_1e_int_kinetic (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->ao_1e_int_group, AO_1E_INT_KINETIC_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_ao_1e_int_potential_n_e (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->ao_1e_int_group, AO_1E_INT_POTENTIAL_N_E_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_ao_1e_int_ecp_local (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->ao_1e_int_group, AO_1E_INT_ECP_LOCAL_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_ao_1e_int_ecp_non_local (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->ao_1e_int_group, AO_1E_INT_ECP_NON_LOCAL_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_ao_1e_int_core_hamiltonian (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->ao_1e_int_group, AO_1E_INT_CORE_HAMILTONIAN_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_ao_2e_int_eri (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->ao_2e_int_group, AO_2E_INT_ERI_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_ao_2e_int_eri_lr (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->ao_2e_int_group, AO_2E_INT_ERI_LR_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_mo_coefficient (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->mo_group, MO_COEFFICIENT_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_mo_occupation (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->mo_group, MO_OCCUPATION_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_mo_1e_int_overlap (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->mo_1e_int_group, MO_1E_INT_OVERLAP_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_mo_1e_int_kinetic (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->mo_1e_int_group, MO_1E_INT_KINETIC_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_mo_1e_int_potential_n_e (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->mo_1e_int_group, MO_1E_INT_POTENTIAL_N_E_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_mo_1e_int_ecp_local (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->mo_1e_int_group, MO_1E_INT_ECP_LOCAL_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_mo_1e_int_ecp_non_local (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->mo_1e_int_group, MO_1E_INT_ECP_NON_LOCAL_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_mo_1e_int_core_hamiltonian (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->mo_1e_int_group, MO_1E_INT_CORE_HAMILTONIAN_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_mo_2e_int_eri (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->mo_2e_int_group, MO_2E_INT_ERI_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_mo_2e_int_eri_lr (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->mo_2e_int_group, MO_2E_INT_ERI_LR_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_metadata_code (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->metadata_group, METADATA_CODE_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_metadata_author (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->metadata_group, METADATA_AUTHOR_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_nucleus_label (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->nucleus_group, NUCLEUS_LABEL_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_mo_class (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->mo_group, MO_CLASS_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_has_mo_symmetry (trexio_t* const file)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status = H5LTfind_dataset(f->mo_group, MO_SYMMETRY_NAME);
  /* H5LTfind_dataset returns 1 if dataset exists, 0 otherwise */
  if (status == 1){
    return TREXIO_SUCCESS;
  } else if (status == 0) {
    return TREXIO_HAS_NOT;
  } else {
    return TREXIO_FAILURE;
  }

}

trexio_exit_code
trexio_hdf5_read_metadata_code_num (trexio_t* const file, int64_t* const num)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (num  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;
  /* Quit if the dimensioning attribute is missing in the file */
  if (H5Aexists(f->metadata_group, METADATA_CODE_NUM_NAME) == 0) return TREXIO_FAILURE;

  /* Read the metadata_code_num attribute of metadata group */
  const hid_t num_id = H5Aopen(f->metadata_group, METADATA_CODE_NUM_NAME, H5P_DEFAULT);
  if (num_id <= 0) return TREXIO_INVALID_ID;

  const herr_t status = H5Aread(num_id, H5T_NATIVE_INT64, num);

  H5Aclose(num_id);

  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_read_metadata_author_num (trexio_t* const file, int64_t* const num)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (num  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;
  /* Quit if the dimensioning attribute is missing in the file */
  if (H5Aexists(f->metadata_group, METADATA_AUTHOR_NUM_NAME) == 0) return TREXIO_FAILURE;

  /* Read the metadata_author_num attribute of metadata group */
  const hid_t num_id = H5Aopen(f->metadata_group, METADATA_AUTHOR_NUM_NAME, H5P_DEFAULT);
  if (num_id <= 0) return TREXIO_INVALID_ID;

  const herr_t status = H5Aread(num_id, H5T_NATIVE_INT64, num);

  H5Aclose(num_id);

  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_read_electron_up_num (trexio_t* const file, int64_t* const num)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (num  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;
  /* Quit if the dimensioning attribute is missing in the file */
  if (H5Aexists(f->electron_group, ELECTRON_UP_NUM_NAME) == 0) return TREXIO_FAILURE;

  /* Read the electron_up_num attribute of electron group */
  const hid_t num_id = H5Aopen(f->electron_group, ELECTRON_UP_NUM_NAME, H5P_DEFAULT);
  if (num_id <= 0) return TREXIO_INVALID_ID;

  const herr_t status = H5Aread(num_id, H5T_NATIVE_INT64, num);

  H5Aclose(num_id);

  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_read_electron_dn_num (trexio_t* const file, int64_t* const num)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (num  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;
  /* Quit if the dimensioning attribute is missing in the file */
  if (H5Aexists(f->electron_group, ELECTRON_DN_NUM_NAME) == 0) return TREXIO_FAILURE;

  /* Read the electron_dn_num attribute of electron group */
  const hid_t num_id = H5Aopen(f->electron_group, ELECTRON_DN_NUM_NAME, H5P_DEFAULT);
  if (num_id <= 0) return TREXIO_INVALID_ID;

  const herr_t status = H5Aread(num_id, H5T_NATIVE_INT64, num);

  H5Aclose(num_id);

  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_read_nucleus_num (trexio_t* const file, int64_t* const num)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (num  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;
  /* Quit if the dimensioning attribute is missing in the file */
  if (H5Aexists(f->nucleus_group, NUCLEUS_NUM_NAME) == 0) return TREXIO_FAILURE;

  /* Read the nucleus_num attribute of nucleus group */
  const hid_t num_id = H5Aopen(f->nucleus_group, NUCLEUS_NUM_NAME, H5P_DEFAULT);
  if (num_id <= 0) return TREXIO_INVALID_ID;

  const herr_t status = H5Aread(num_id, H5T_NATIVE_INT64, num);

  H5Aclose(num_id);

  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_read_ecp_num (trexio_t* const file, int64_t* const num)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (num  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;
  /* Quit if the dimensioning attribute is missing in the file */
  if (H5Aexists(f->ecp_group, ECP_NUM_NAME) == 0) return TREXIO_FAILURE;

  /* Read the ecp_num attribute of ecp group */
  const hid_t num_id = H5Aopen(f->ecp_group, ECP_NUM_NAME, H5P_DEFAULT);
  if (num_id <= 0) return TREXIO_INVALID_ID;

  const herr_t status = H5Aread(num_id, H5T_NATIVE_INT64, num);

  H5Aclose(num_id);

  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_read_basis_prim_num (trexio_t* const file, int64_t* const num)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (num  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;
  /* Quit if the dimensioning attribute is missing in the file */
  if (H5Aexists(f->basis_group, BASIS_PRIM_NUM_NAME) == 0) return TREXIO_FAILURE;

  /* Read the basis_prim_num attribute of basis group */
  const hid_t num_id = H5Aopen(f->basis_group, BASIS_PRIM_NUM_NAME, H5P_DEFAULT);
  if (num_id <= 0) return TREXIO_INVALID_ID;

  const herr_t status = H5Aread(num_id, H5T_NATIVE_INT64, num);

  H5Aclose(num_id);

  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_read_basis_shell_num (trexio_t* const file, int64_t* const num)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (num  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;
  /* Quit if the dimensioning attribute is missing in the file */
  if (H5Aexists(f->basis_group, BASIS_SHELL_NUM_NAME) == 0) return TREXIO_FAILURE;

  /* Read the basis_shell_num attribute of basis group */
  const hid_t num_id = H5Aopen(f->basis_group, BASIS_SHELL_NUM_NAME, H5P_DEFAULT);
  if (num_id <= 0) return TREXIO_INVALID_ID;

  const herr_t status = H5Aread(num_id, H5T_NATIVE_INT64, num);

  H5Aclose(num_id);

  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_read_ao_cartesian (trexio_t* const file, int64_t* const num)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (num  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;
  /* Quit if the dimensioning attribute is missing in the file */
  if (H5Aexists(f->ao_group, AO_CARTESIAN_NAME) == 0) return TREXIO_FAILURE;

  /* Read the ao_cartesian attribute of ao group */
  const hid_t num_id = H5Aopen(f->ao_group, AO_CARTESIAN_NAME, H5P_DEFAULT);
  if (num_id <= 0) return TREXIO_INVALID_ID;

  const herr_t status = H5Aread(num_id, H5T_NATIVE_INT64, num);

  H5Aclose(num_id);

  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_read_ao_num (trexio_t* const file, int64_t* const num)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (num  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;
  /* Quit if the dimensioning attribute is missing in the file */
  if (H5Aexists(f->ao_group, AO_NUM_NAME) == 0) return TREXIO_FAILURE;

  /* Read the ao_num attribute of ao group */
  const hid_t num_id = H5Aopen(f->ao_group, AO_NUM_NAME, H5P_DEFAULT);
  if (num_id <= 0) return TREXIO_INVALID_ID;

  const herr_t status = H5Aread(num_id, H5T_NATIVE_INT64, num);

  H5Aclose(num_id);

  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_read_mo_num (trexio_t* const file, int64_t* const num)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (num  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;
  /* Quit if the dimensioning attribute is missing in the file */
  if (H5Aexists(f->mo_group, MO_NUM_NAME) == 0) return TREXIO_FAILURE;

  /* Read the mo_num attribute of mo group */
  const hid_t num_id = H5Aopen(f->mo_group, MO_NUM_NAME, H5P_DEFAULT);
  if (num_id <= 0) return TREXIO_INVALID_ID;

  const herr_t status = H5Aread(num_id, H5T_NATIVE_INT64, num);

  H5Aclose(num_id);

  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_read_metadata_package_version (trexio_t* const file, char* const str, const uint32_t max_str_len)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (str  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;
  /* Quit if the string attribute is missing in the file */
  if (H5Aexists(f->metadata_group, METADATA_PACKAGE_VERSION_NAME) == 0) return TREXIO_HAS_NOT;

  /* Read the metadata_package_version attribute of metadata group */
  const hid_t str_id = H5Aopen(f->metadata_group, METADATA_PACKAGE_VERSION_NAME, H5P_DEFAULT);
  if (str_id <= 0) return TREXIO_INVALID_ID;

  const hid_t ftype_id = H5Aget_type(str_id);
  if (ftype_id <= 0) return TREXIO_INVALID_ID;
  uint64_t sdim = H5Tget_size(ftype_id);
  if (sdim <= 0) return TREXIO_FAILURE;
  sdim++;                         /* Make room for null terminator */

  const hid_t mem_id = H5Tcopy(H5T_C_S1);
  if (mem_id <= 0) return TREXIO_INVALID_ID;

  herr_t status;
  status = (max_str_len+1) > sdim ? H5Tset_size(mem_id, sdim) : H5Tset_size(mem_id, max_str_len+1) ;
  if (status < 0) return TREXIO_FAILURE;

  status = H5Aread(str_id, mem_id, str);
  if (status < 0) return TREXIO_FAILURE;

  H5Aclose(str_id);
  H5Tclose(mem_id);
  H5Tclose(ftype_id);

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_read_metadata_description (trexio_t* const file, char* const str, const uint32_t max_str_len)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (str  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;
  /* Quit if the string attribute is missing in the file */
  if (H5Aexists(f->metadata_group, METADATA_DESCRIPTION_NAME) == 0) return TREXIO_HAS_NOT;

  /* Read the metadata_description attribute of metadata group */
  const hid_t str_id = H5Aopen(f->metadata_group, METADATA_DESCRIPTION_NAME, H5P_DEFAULT);
  if (str_id <= 0) return TREXIO_INVALID_ID;

  const hid_t ftype_id = H5Aget_type(str_id);
  if (ftype_id <= 0) return TREXIO_INVALID_ID;
  uint64_t sdim = H5Tget_size(ftype_id);
  if (sdim <= 0) return TREXIO_FAILURE;
  sdim++;                         /* Make room for null terminator */

  const hid_t mem_id = H5Tcopy(H5T_C_S1);
  if (mem_id <= 0) return TREXIO_INVALID_ID;

  herr_t status;
  status = (max_str_len+1) > sdim ? H5Tset_size(mem_id, sdim) : H5Tset_size(mem_id, max_str_len+1) ;
  if (status < 0) return TREXIO_FAILURE;

  status = H5Aread(str_id, mem_id, str);
  if (status < 0) return TREXIO_FAILURE;

  H5Aclose(str_id);
  H5Tclose(mem_id);
  H5Tclose(ftype_id);

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_read_nucleus_point_group (trexio_t* const file, char* const str, const uint32_t max_str_len)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (str  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;
  /* Quit if the string attribute is missing in the file */
  if (H5Aexists(f->nucleus_group, NUCLEUS_POINT_GROUP_NAME) == 0) return TREXIO_HAS_NOT;

  /* Read the nucleus_point_group attribute of nucleus group */
  const hid_t str_id = H5Aopen(f->nucleus_group, NUCLEUS_POINT_GROUP_NAME, H5P_DEFAULT);
  if (str_id <= 0) return TREXIO_INVALID_ID;

  const hid_t ftype_id = H5Aget_type(str_id);
  if (ftype_id <= 0) return TREXIO_INVALID_ID;
  uint64_t sdim = H5Tget_size(ftype_id);
  if (sdim <= 0) return TREXIO_FAILURE;
  sdim++;                         /* Make room for null terminator */

  const hid_t mem_id = H5Tcopy(H5T_C_S1);
  if (mem_id <= 0) return TREXIO_INVALID_ID;

  herr_t status;
  status = (max_str_len+1) > sdim ? H5Tset_size(mem_id, sdim) : H5Tset_size(mem_id, max_str_len+1) ;
  if (status < 0) return TREXIO_FAILURE;

  status = H5Aread(str_id, mem_id, str);
  if (status < 0) return TREXIO_FAILURE;

  H5Aclose(str_id);
  H5Tclose(mem_id);
  H5Tclose(ftype_id);

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_read_basis_type (trexio_t* const file, char* const str, const uint32_t max_str_len)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (str  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;
  /* Quit if the string attribute is missing in the file */
  if (H5Aexists(f->basis_group, BASIS_TYPE_NAME) == 0) return TREXIO_HAS_NOT;

  /* Read the basis_type attribute of basis group */
  const hid_t str_id = H5Aopen(f->basis_group, BASIS_TYPE_NAME, H5P_DEFAULT);
  if (str_id <= 0) return TREXIO_INVALID_ID;

  const hid_t ftype_id = H5Aget_type(str_id);
  if (ftype_id <= 0) return TREXIO_INVALID_ID;
  uint64_t sdim = H5Tget_size(ftype_id);
  if (sdim <= 0) return TREXIO_FAILURE;
  sdim++;                         /* Make room for null terminator */

  const hid_t mem_id = H5Tcopy(H5T_C_S1);
  if (mem_id <= 0) return TREXIO_INVALID_ID;

  herr_t status;
  status = (max_str_len+1) > sdim ? H5Tset_size(mem_id, sdim) : H5Tset_size(mem_id, max_str_len+1) ;
  if (status < 0) return TREXIO_FAILURE;

  status = H5Aread(str_id, mem_id, str);
  if (status < 0) return TREXIO_FAILURE;

  H5Aclose(str_id);
  H5Tclose(mem_id);
  H5Tclose(ftype_id);

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_read_mo_type (trexio_t* const file, char* const str, const uint32_t max_str_len)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (str  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;
  /* Quit if the string attribute is missing in the file */
  if (H5Aexists(f->mo_group, MO_TYPE_NAME) == 0) return TREXIO_HAS_NOT;

  /* Read the mo_type attribute of mo group */
  const hid_t str_id = H5Aopen(f->mo_group, MO_TYPE_NAME, H5P_DEFAULT);
  if (str_id <= 0) return TREXIO_INVALID_ID;

  const hid_t ftype_id = H5Aget_type(str_id);
  if (ftype_id <= 0) return TREXIO_INVALID_ID;
  uint64_t sdim = H5Tget_size(ftype_id);
  if (sdim <= 0) return TREXIO_FAILURE;
  sdim++;                         /* Make room for null terminator */

  const hid_t mem_id = H5Tcopy(H5T_C_S1);
  if (mem_id <= 0) return TREXIO_INVALID_ID;

  herr_t status;
  status = (max_str_len+1) > sdim ? H5Tset_size(mem_id, sdim) : H5Tset_size(mem_id, max_str_len+1) ;
  if (status < 0) return TREXIO_FAILURE;

  status = H5Aread(str_id, mem_id, str);
  if (status < 0) return TREXIO_FAILURE;

  H5Aclose(str_id);
  H5Tclose(mem_id);
  H5Tclose(ftype_id);

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_read_nucleus_charge (trexio_t* const file, double* const nucleus_charge, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (nucleus_charge  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->nucleus_group, NUCLEUS_CHARGE_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->nucleus_group,
			           NUCLEUS_CHARGE_NAME,
			           H5T_NATIVE_DOUBLE,
			           nucleus_charge);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_nucleus_coord (trexio_t* const file, double* const nucleus_coord, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (nucleus_coord  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->nucleus_group, NUCLEUS_COORD_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->nucleus_group,
			           NUCLEUS_COORD_NAME,
			           H5T_NATIVE_DOUBLE,
			           nucleus_coord);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_ecp_max_ang_mom_plus_1 (trexio_t* const file, int64_t* const ecp_max_ang_mom_plus_1, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ecp_max_ang_mom_plus_1  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->ecp_group, ECP_MAX_ANG_MOM_PLUS_1_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->ecp_group,
			           ECP_MAX_ANG_MOM_PLUS_1_NAME,
			           H5T_NATIVE_INT64,
			           ecp_max_ang_mom_plus_1);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_ecp_z_core (trexio_t* const file, int64_t* const ecp_z_core, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ecp_z_core  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->ecp_group, ECP_Z_CORE_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->ecp_group,
			           ECP_Z_CORE_NAME,
			           H5T_NATIVE_INT64,
			           ecp_z_core);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_ecp_ang_mom (trexio_t* const file, int64_t* const ecp_ang_mom, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ecp_ang_mom  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->ecp_group, ECP_ANG_MOM_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->ecp_group,
			           ECP_ANG_MOM_NAME,
			           H5T_NATIVE_INT64,
			           ecp_ang_mom);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_ecp_nucleus_index (trexio_t* const file, int64_t* const ecp_nucleus_index, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ecp_nucleus_index  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->ecp_group, ECP_NUCLEUS_INDEX_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->ecp_group,
			           ECP_NUCLEUS_INDEX_NAME,
			           H5T_NATIVE_INT64,
			           ecp_nucleus_index);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_ecp_exponent (trexio_t* const file, double* const ecp_exponent, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ecp_exponent  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->ecp_group, ECP_EXPONENT_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->ecp_group,
			           ECP_EXPONENT_NAME,
			           H5T_NATIVE_DOUBLE,
			           ecp_exponent);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_ecp_coefficient (trexio_t* const file, double* const ecp_coefficient, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ecp_coefficient  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->ecp_group, ECP_COEFFICIENT_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->ecp_group,
			           ECP_COEFFICIENT_NAME,
			           H5T_NATIVE_DOUBLE,
			           ecp_coefficient);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_ecp_power (trexio_t* const file, int64_t* const ecp_power, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ecp_power  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->ecp_group, ECP_POWER_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->ecp_group,
			           ECP_POWER_NAME,
			           H5T_NATIVE_INT64,
			           ecp_power);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_basis_nucleus_index (trexio_t* const file, int64_t* const basis_nucleus_index, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (basis_nucleus_index  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->basis_group, BASIS_NUCLEUS_INDEX_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->basis_group,
			           BASIS_NUCLEUS_INDEX_NAME,
			           H5T_NATIVE_INT64,
			           basis_nucleus_index);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_basis_shell_ang_mom (trexio_t* const file, int64_t* const basis_shell_ang_mom, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (basis_shell_ang_mom  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->basis_group, BASIS_SHELL_ANG_MOM_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->basis_group,
			           BASIS_SHELL_ANG_MOM_NAME,
			           H5T_NATIVE_INT64,
			           basis_shell_ang_mom);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_basis_shell_factor (trexio_t* const file, double* const basis_shell_factor, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (basis_shell_factor  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->basis_group, BASIS_SHELL_FACTOR_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->basis_group,
			           BASIS_SHELL_FACTOR_NAME,
			           H5T_NATIVE_DOUBLE,
			           basis_shell_factor);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_basis_shell_index (trexio_t* const file, int64_t* const basis_shell_index, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (basis_shell_index  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->basis_group, BASIS_SHELL_INDEX_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->basis_group,
			           BASIS_SHELL_INDEX_NAME,
			           H5T_NATIVE_INT64,
			           basis_shell_index);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_basis_exponent (trexio_t* const file, double* const basis_exponent, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (basis_exponent  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->basis_group, BASIS_EXPONENT_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->basis_group,
			           BASIS_EXPONENT_NAME,
			           H5T_NATIVE_DOUBLE,
			           basis_exponent);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_basis_coefficient (trexio_t* const file, double* const basis_coefficient, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (basis_coefficient  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->basis_group, BASIS_COEFFICIENT_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->basis_group,
			           BASIS_COEFFICIENT_NAME,
			           H5T_NATIVE_DOUBLE,
			           basis_coefficient);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_basis_prim_factor (trexio_t* const file, double* const basis_prim_factor, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (basis_prim_factor  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->basis_group, BASIS_PRIM_FACTOR_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->basis_group,
			           BASIS_PRIM_FACTOR_NAME,
			           H5T_NATIVE_DOUBLE,
			           basis_prim_factor);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_ao_shell (trexio_t* const file, int64_t* const ao_shell, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ao_shell  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->ao_group, AO_SHELL_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->ao_group,
			           AO_SHELL_NAME,
			           H5T_NATIVE_INT64,
			           ao_shell);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_ao_normalization (trexio_t* const file, double* const ao_normalization, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ao_normalization  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->ao_group, AO_NORMALIZATION_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->ao_group,
			           AO_NORMALIZATION_NAME,
			           H5T_NATIVE_DOUBLE,
			           ao_normalization);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_ao_1e_int_overlap (trexio_t* const file, double* const ao_1e_int_overlap, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ao_1e_int_overlap  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->ao_1e_int_group, AO_1E_INT_OVERLAP_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->ao_1e_int_group,
			           AO_1E_INT_OVERLAP_NAME,
			           H5T_NATIVE_DOUBLE,
			           ao_1e_int_overlap);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_ao_1e_int_kinetic (trexio_t* const file, double* const ao_1e_int_kinetic, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ao_1e_int_kinetic  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->ao_1e_int_group, AO_1E_INT_KINETIC_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->ao_1e_int_group,
			           AO_1E_INT_KINETIC_NAME,
			           H5T_NATIVE_DOUBLE,
			           ao_1e_int_kinetic);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_ao_1e_int_potential_n_e (trexio_t* const file, double* const ao_1e_int_potential_n_e, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ao_1e_int_potential_n_e  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->ao_1e_int_group, AO_1E_INT_POTENTIAL_N_E_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->ao_1e_int_group,
			           AO_1E_INT_POTENTIAL_N_E_NAME,
			           H5T_NATIVE_DOUBLE,
			           ao_1e_int_potential_n_e);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_ao_1e_int_ecp_local (trexio_t* const file, double* const ao_1e_int_ecp_local, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ao_1e_int_ecp_local  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->ao_1e_int_group, AO_1E_INT_ECP_LOCAL_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->ao_1e_int_group,
			           AO_1E_INT_ECP_LOCAL_NAME,
			           H5T_NATIVE_DOUBLE,
			           ao_1e_int_ecp_local);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_ao_1e_int_ecp_non_local (trexio_t* const file, double* const ao_1e_int_ecp_non_local, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ao_1e_int_ecp_non_local  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->ao_1e_int_group, AO_1E_INT_ECP_NON_LOCAL_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->ao_1e_int_group,
			           AO_1E_INT_ECP_NON_LOCAL_NAME,
			           H5T_NATIVE_DOUBLE,
			           ao_1e_int_ecp_non_local);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_ao_1e_int_core_hamiltonian (trexio_t* const file, double* const ao_1e_int_core_hamiltonian, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ao_1e_int_core_hamiltonian  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->ao_1e_int_group, AO_1E_INT_CORE_HAMILTONIAN_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->ao_1e_int_group,
			           AO_1E_INT_CORE_HAMILTONIAN_NAME,
			           H5T_NATIVE_DOUBLE,
			           ao_1e_int_core_hamiltonian);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_ao_2e_int_eri (trexio_t* const file, double* const ao_2e_int_eri, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ao_2e_int_eri  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->ao_2e_int_group, AO_2E_INT_ERI_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->ao_2e_int_group,
			           AO_2E_INT_ERI_NAME,
			           H5T_NATIVE_DOUBLE,
			           ao_2e_int_eri);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_ao_2e_int_eri_lr (trexio_t* const file, double* const ao_2e_int_eri_lr, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ao_2e_int_eri_lr  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->ao_2e_int_group, AO_2E_INT_ERI_LR_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->ao_2e_int_group,
			           AO_2E_INT_ERI_LR_NAME,
			           H5T_NATIVE_DOUBLE,
			           ao_2e_int_eri_lr);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_mo_coefficient (trexio_t* const file, double* const mo_coefficient, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_coefficient  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->mo_group, MO_COEFFICIENT_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->mo_group,
			           MO_COEFFICIENT_NAME,
			           H5T_NATIVE_DOUBLE,
			           mo_coefficient);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_mo_occupation (trexio_t* const file, double* const mo_occupation, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_occupation  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->mo_group, MO_OCCUPATION_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->mo_group,
			           MO_OCCUPATION_NAME,
			           H5T_NATIVE_DOUBLE,
			           mo_occupation);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_mo_1e_int_overlap (trexio_t* const file, double* const mo_1e_int_overlap, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_1e_int_overlap  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->mo_1e_int_group, MO_1E_INT_OVERLAP_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->mo_1e_int_group,
			           MO_1E_INT_OVERLAP_NAME,
			           H5T_NATIVE_DOUBLE,
			           mo_1e_int_overlap);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_mo_1e_int_kinetic (trexio_t* const file, double* const mo_1e_int_kinetic, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_1e_int_kinetic  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->mo_1e_int_group, MO_1E_INT_KINETIC_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->mo_1e_int_group,
			           MO_1E_INT_KINETIC_NAME,
			           H5T_NATIVE_DOUBLE,
			           mo_1e_int_kinetic);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_mo_1e_int_potential_n_e (trexio_t* const file, double* const mo_1e_int_potential_n_e, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_1e_int_potential_n_e  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->mo_1e_int_group, MO_1E_INT_POTENTIAL_N_E_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->mo_1e_int_group,
			           MO_1E_INT_POTENTIAL_N_E_NAME,
			           H5T_NATIVE_DOUBLE,
			           mo_1e_int_potential_n_e);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_mo_1e_int_ecp_local (trexio_t* const file, double* const mo_1e_int_ecp_local, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_1e_int_ecp_local  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->mo_1e_int_group, MO_1E_INT_ECP_LOCAL_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->mo_1e_int_group,
			           MO_1E_INT_ECP_LOCAL_NAME,
			           H5T_NATIVE_DOUBLE,
			           mo_1e_int_ecp_local);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_mo_1e_int_ecp_non_local (trexio_t* const file, double* const mo_1e_int_ecp_non_local, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_1e_int_ecp_non_local  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->mo_1e_int_group, MO_1E_INT_ECP_NON_LOCAL_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->mo_1e_int_group,
			           MO_1E_INT_ECP_NON_LOCAL_NAME,
			           H5T_NATIVE_DOUBLE,
			           mo_1e_int_ecp_non_local);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_mo_1e_int_core_hamiltonian (trexio_t* const file, double* const mo_1e_int_core_hamiltonian, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_1e_int_core_hamiltonian  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->mo_1e_int_group, MO_1E_INT_CORE_HAMILTONIAN_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->mo_1e_int_group,
			           MO_1E_INT_CORE_HAMILTONIAN_NAME,
			           H5T_NATIVE_DOUBLE,
			           mo_1e_int_core_hamiltonian);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_mo_2e_int_eri (trexio_t* const file, double* const mo_2e_int_eri, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_2e_int_eri  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->mo_2e_int_group, MO_2E_INT_ERI_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->mo_2e_int_group,
			           MO_2E_INT_ERI_NAME,
			           H5T_NATIVE_DOUBLE,
			           mo_2e_int_eri);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_mo_2e_int_eri_lr (trexio_t* const file, double* const mo_2e_int_eri_lr, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_2e_int_eri_lr  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->mo_2e_int_group, MO_2E_INT_ERI_LR_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) return TREXIO_FAILURE;

  // get the dataspace of the dataset
  hid_t dspace_id = H5Dget_space(dset_id);
  // get the rank and dimensions of the dataset
  int rrank = H5Sget_simple_extent_dims(dspace_id, ddims, NULL);

  // check that dimensions are consistent
  if (rrank != (int) rank) {
    FREE(ddims);
    H5Sclose(dspace_id);
    H5Dclose(dset_id);
    return TREXIO_INVALID_ARG_3;
  }

  for (uint32_t i=0; i<rank; ++i){
    if (ddims[i] != dims[i]) {
      FREE(ddims);
      H5Sclose(dspace_id);
      H5Dclose(dset_id);
      return TREXIO_INVALID_ARG_4;
    }
  }

  FREE(ddims);
  H5Sclose(dspace_id);
  H5Dclose(dset_id);

  /* High-level H5LT API. No need to deal with dataspaces and datatypes */
  herr_t status = H5LTread_dataset(f->mo_2e_int_group,
			           MO_2E_INT_ERI_LR_NAME,
			           H5T_NATIVE_DOUBLE,
			           mo_2e_int_eri_lr);
  if (status < 0) return TREXIO_FAILURE;

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_metadata_code (trexio_t* const file, char* const metadata_code, const uint32_t rank, const uint64_t* dims, const uint32_t max_str_len)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (metadata_code  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  herr_t status;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->metadata_group, METADATA_CODE_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) {
    H5Dclose(dset_id);
    return TREXIO_ALLOCATION_FAILED;
  }

  hid_t dspace = H5Dget_space(dset_id); 
  if (dset_id <= 0) {
    FREE(ddims);
    H5Dclose(dset_id); 
    return TREXIO_INVALID_ID;
  }

  // get the rank of the dataset in a file
  int rrank = H5Sget_simple_extent_dims(dspace, ddims, NULL);

  if (rrank != (int) rank) {
    FREE(ddims);
    H5Dclose(dset_id);
    H5Sclose(dspace);
    return TREXIO_INVALID_ARG_3;
  }

  for (int i=0; i<rrank; i++) {
    if (ddims[i] != dims[i]) {
      H5Dclose(dset_id);
      H5Sclose(dspace);
      FREE(ddims);
      return TREXIO_INVALID_ARG_4;
    }
  }
  FREE(ddims);

  hid_t memtype = H5Tcopy (H5T_C_S1);
  status = H5Tset_size(memtype, H5T_VARIABLE);
  if (status < 0 || memtype <= 0) {
    H5Dclose(dset_id);
    H5Sclose(dspace);
    return TREXIO_FAILURE;
  }

  char** rdata = CALLOC(dims[0], char*);
  if (rdata == NULL) {
    H5Dclose(dset_id);
    H5Sclose(dspace);
    H5Tclose(memtype); 
    return TREXIO_ALLOCATION_FAILED;
  }

  status = H5Dread(dset_id, memtype, H5S_ALL, H5S_ALL, H5P_DEFAULT, rdata);
  if (status < 0) {
    FREE(rdata);
    H5Dclose(dset_id);
    H5Sclose(dspace);
    H5Tclose(memtype); 
    return TREXIO_FAILURE;
  }

  // copy contents of temporary rdata buffer into the group_dset otherwise they are lost
  // after calling H5Treclaim or H5Dvlen_reclaim functions
  strcpy(metadata_code, "");
  for (uint64_t i=0; i<dims[0]; i++) {
    strncat(metadata_code, rdata[i], max_str_len);
    strcat(metadata_code, TREXIO_DELIM);
  }

  // H5Dvlen_reclaim is deprecated and replaced by H5Treclaim in HDF5 v.1.12.0
  #if (H5_VERS_MAJOR <= 1 && H5_VERS_MINOR < 12)
    status = H5Dvlen_reclaim(memtype, dspace, H5P_DEFAULT, rdata);
  #else
    status = H5Treclaim(memtype, dspace, H5P_DEFAULT, rdata);
  #endif

  if (status < 0) {
    FREE(rdata);
    H5Dclose(dset_id);
    H5Sclose(dspace);
    H5Tclose(memtype); 
    return TREXIO_FAILURE;
  }

  FREE(rdata); 
  H5Dclose(dset_id);
  H5Sclose(dspace);
  H5Tclose(memtype);

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_metadata_author (trexio_t* const file, char* const metadata_author, const uint32_t rank, const uint64_t* dims, const uint32_t max_str_len)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (metadata_author  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  herr_t status;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->metadata_group, METADATA_AUTHOR_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) {
    H5Dclose(dset_id);
    return TREXIO_ALLOCATION_FAILED;
  }

  hid_t dspace = H5Dget_space(dset_id); 
  if (dset_id <= 0) {
    FREE(ddims);
    H5Dclose(dset_id); 
    return TREXIO_INVALID_ID;
  }

  // get the rank of the dataset in a file
  int rrank = H5Sget_simple_extent_dims(dspace, ddims, NULL);

  if (rrank != (int) rank) {
    FREE(ddims);
    H5Dclose(dset_id);
    H5Sclose(dspace);
    return TREXIO_INVALID_ARG_3;
  }

  for (int i=0; i<rrank; i++) {
    if (ddims[i] != dims[i]) {
      H5Dclose(dset_id);
      H5Sclose(dspace);
      FREE(ddims);
      return TREXIO_INVALID_ARG_4;
    }
  }
  FREE(ddims);

  hid_t memtype = H5Tcopy (H5T_C_S1);
  status = H5Tset_size(memtype, H5T_VARIABLE);
  if (status < 0 || memtype <= 0) {
    H5Dclose(dset_id);
    H5Sclose(dspace);
    return TREXIO_FAILURE;
  }

  char** rdata = CALLOC(dims[0], char*);
  if (rdata == NULL) {
    H5Dclose(dset_id);
    H5Sclose(dspace);
    H5Tclose(memtype); 
    return TREXIO_ALLOCATION_FAILED;
  }

  status = H5Dread(dset_id, memtype, H5S_ALL, H5S_ALL, H5P_DEFAULT, rdata);
  if (status < 0) {
    FREE(rdata);
    H5Dclose(dset_id);
    H5Sclose(dspace);
    H5Tclose(memtype); 
    return TREXIO_FAILURE;
  }

  // copy contents of temporary rdata buffer into the group_dset otherwise they are lost
  // after calling H5Treclaim or H5Dvlen_reclaim functions
  strcpy(metadata_author, "");
  for (uint64_t i=0; i<dims[0]; i++) {
    strncat(metadata_author, rdata[i], max_str_len);
    strcat(metadata_author, TREXIO_DELIM);
  }

  // H5Dvlen_reclaim is deprecated and replaced by H5Treclaim in HDF5 v.1.12.0
  #if (H5_VERS_MAJOR <= 1 && H5_VERS_MINOR < 12)
    status = H5Dvlen_reclaim(memtype, dspace, H5P_DEFAULT, rdata);
  #else
    status = H5Treclaim(memtype, dspace, H5P_DEFAULT, rdata);
  #endif

  if (status < 0) {
    FREE(rdata);
    H5Dclose(dset_id);
    H5Sclose(dspace);
    H5Tclose(memtype); 
    return TREXIO_FAILURE;
  }

  FREE(rdata); 
  H5Dclose(dset_id);
  H5Sclose(dspace);
  H5Tclose(memtype);

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_nucleus_label (trexio_t* const file, char* const nucleus_label, const uint32_t rank, const uint64_t* dims, const uint32_t max_str_len)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (nucleus_label  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  herr_t status;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->nucleus_group, NUCLEUS_LABEL_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) {
    H5Dclose(dset_id);
    return TREXIO_ALLOCATION_FAILED;
  }

  hid_t dspace = H5Dget_space(dset_id); 
  if (dset_id <= 0) {
    FREE(ddims);
    H5Dclose(dset_id); 
    return TREXIO_INVALID_ID;
  }

  // get the rank of the dataset in a file
  int rrank = H5Sget_simple_extent_dims(dspace, ddims, NULL);

  if (rrank != (int) rank) {
    FREE(ddims);
    H5Dclose(dset_id);
    H5Sclose(dspace);
    return TREXIO_INVALID_ARG_3;
  }

  for (int i=0; i<rrank; i++) {
    if (ddims[i] != dims[i]) {
      H5Dclose(dset_id);
      H5Sclose(dspace);
      FREE(ddims);
      return TREXIO_INVALID_ARG_4;
    }
  }
  FREE(ddims);

  hid_t memtype = H5Tcopy (H5T_C_S1);
  status = H5Tset_size(memtype, H5T_VARIABLE);
  if (status < 0 || memtype <= 0) {
    H5Dclose(dset_id);
    H5Sclose(dspace);
    return TREXIO_FAILURE;
  }

  char** rdata = CALLOC(dims[0], char*);
  if (rdata == NULL) {
    H5Dclose(dset_id);
    H5Sclose(dspace);
    H5Tclose(memtype); 
    return TREXIO_ALLOCATION_FAILED;
  }

  status = H5Dread(dset_id, memtype, H5S_ALL, H5S_ALL, H5P_DEFAULT, rdata);
  if (status < 0) {
    FREE(rdata);
    H5Dclose(dset_id);
    H5Sclose(dspace);
    H5Tclose(memtype); 
    return TREXIO_FAILURE;
  }

  // copy contents of temporary rdata buffer into the group_dset otherwise they are lost
  // after calling H5Treclaim or H5Dvlen_reclaim functions
  strcpy(nucleus_label, "");
  for (uint64_t i=0; i<dims[0]; i++) {
    strncat(nucleus_label, rdata[i], max_str_len);
    strcat(nucleus_label, TREXIO_DELIM);
  }

  // H5Dvlen_reclaim is deprecated and replaced by H5Treclaim in HDF5 v.1.12.0
  #if (H5_VERS_MAJOR <= 1 && H5_VERS_MINOR < 12)
    status = H5Dvlen_reclaim(memtype, dspace, H5P_DEFAULT, rdata);
  #else
    status = H5Treclaim(memtype, dspace, H5P_DEFAULT, rdata);
  #endif

  if (status < 0) {
    FREE(rdata);
    H5Dclose(dset_id);
    H5Sclose(dspace);
    H5Tclose(memtype); 
    return TREXIO_FAILURE;
  }

  FREE(rdata); 
  H5Dclose(dset_id);
  H5Sclose(dspace);
  H5Tclose(memtype);

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_mo_class (trexio_t* const file, char* const mo_class, const uint32_t rank, const uint64_t* dims, const uint32_t max_str_len)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_class  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  herr_t status;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->mo_group, MO_CLASS_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) {
    H5Dclose(dset_id);
    return TREXIO_ALLOCATION_FAILED;
  }

  hid_t dspace = H5Dget_space(dset_id); 
  if (dset_id <= 0) {
    FREE(ddims);
    H5Dclose(dset_id); 
    return TREXIO_INVALID_ID;
  }

  // get the rank of the dataset in a file
  int rrank = H5Sget_simple_extent_dims(dspace, ddims, NULL);

  if (rrank != (int) rank) {
    FREE(ddims);
    H5Dclose(dset_id);
    H5Sclose(dspace);
    return TREXIO_INVALID_ARG_3;
  }

  for (int i=0; i<rrank; i++) {
    if (ddims[i] != dims[i]) {
      H5Dclose(dset_id);
      H5Sclose(dspace);
      FREE(ddims);
      return TREXIO_INVALID_ARG_4;
    }
  }
  FREE(ddims);

  hid_t memtype = H5Tcopy (H5T_C_S1);
  status = H5Tset_size(memtype, H5T_VARIABLE);
  if (status < 0 || memtype <= 0) {
    H5Dclose(dset_id);
    H5Sclose(dspace);
    return TREXIO_FAILURE;
  }

  char** rdata = CALLOC(dims[0], char*);
  if (rdata == NULL) {
    H5Dclose(dset_id);
    H5Sclose(dspace);
    H5Tclose(memtype); 
    return TREXIO_ALLOCATION_FAILED;
  }

  status = H5Dread(dset_id, memtype, H5S_ALL, H5S_ALL, H5P_DEFAULT, rdata);
  if (status < 0) {
    FREE(rdata);
    H5Dclose(dset_id);
    H5Sclose(dspace);
    H5Tclose(memtype); 
    return TREXIO_FAILURE;
  }

  // copy contents of temporary rdata buffer into the group_dset otherwise they are lost
  // after calling H5Treclaim or H5Dvlen_reclaim functions
  strcpy(mo_class, "");
  for (uint64_t i=0; i<dims[0]; i++) {
    strncat(mo_class, rdata[i], max_str_len);
    strcat(mo_class, TREXIO_DELIM);
  }

  // H5Dvlen_reclaim is deprecated and replaced by H5Treclaim in HDF5 v.1.12.0
  #if (H5_VERS_MAJOR <= 1 && H5_VERS_MINOR < 12)
    status = H5Dvlen_reclaim(memtype, dspace, H5P_DEFAULT, rdata);
  #else
    status = H5Treclaim(memtype, dspace, H5P_DEFAULT, rdata);
  #endif

  if (status < 0) {
    FREE(rdata);
    H5Dclose(dset_id);
    H5Sclose(dspace);
    H5Tclose(memtype); 
    return TREXIO_FAILURE;
  }

  FREE(rdata); 
  H5Dclose(dset_id);
  H5Sclose(dspace);
  H5Tclose(memtype);

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_read_mo_symmetry (trexio_t* const file, char* const mo_symmetry, const uint32_t rank, const uint64_t* dims, const uint32_t max_str_len)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_symmetry  == NULL) return TREXIO_INVALID_ARG_2;

  const trexio_hdf5_t* f = (const trexio_hdf5_t*) file;

  herr_t status;

  // open the dataset to get its dimensions
  hid_t dset_id = H5Dopen(f->mo_group, MO_SYMMETRY_NAME, H5P_DEFAULT);
  if (dset_id <= 0) return TREXIO_INVALID_ID;

  // allocate space for the dimensions to be read
  hsize_t* ddims = CALLOC( (int) rank, hsize_t);
  if (ddims == NULL) {
    H5Dclose(dset_id);
    return TREXIO_ALLOCATION_FAILED;
  }

  hid_t dspace = H5Dget_space(dset_id); 
  if (dset_id <= 0) {
    FREE(ddims);
    H5Dclose(dset_id); 
    return TREXIO_INVALID_ID;
  }

  // get the rank of the dataset in a file
  int rrank = H5Sget_simple_extent_dims(dspace, ddims, NULL);

  if (rrank != (int) rank) {
    FREE(ddims);
    H5Dclose(dset_id);
    H5Sclose(dspace);
    return TREXIO_INVALID_ARG_3;
  }

  for (int i=0; i<rrank; i++) {
    if (ddims[i] != dims[i]) {
      H5Dclose(dset_id);
      H5Sclose(dspace);
      FREE(ddims);
      return TREXIO_INVALID_ARG_4;
    }
  }
  FREE(ddims);

  hid_t memtype = H5Tcopy (H5T_C_S1);
  status = H5Tset_size(memtype, H5T_VARIABLE);
  if (status < 0 || memtype <= 0) {
    H5Dclose(dset_id);
    H5Sclose(dspace);
    return TREXIO_FAILURE;
  }

  char** rdata = CALLOC(dims[0], char*);
  if (rdata == NULL) {
    H5Dclose(dset_id);
    H5Sclose(dspace);
    H5Tclose(memtype); 
    return TREXIO_ALLOCATION_FAILED;
  }

  status = H5Dread(dset_id, memtype, H5S_ALL, H5S_ALL, H5P_DEFAULT, rdata);
  if (status < 0) {
    FREE(rdata);
    H5Dclose(dset_id);
    H5Sclose(dspace);
    H5Tclose(memtype); 
    return TREXIO_FAILURE;
  }

  // copy contents of temporary rdata buffer into the group_dset otherwise they are lost
  // after calling H5Treclaim or H5Dvlen_reclaim functions
  strcpy(mo_symmetry, "");
  for (uint64_t i=0; i<dims[0]; i++) {
    strncat(mo_symmetry, rdata[i], max_str_len);
    strcat(mo_symmetry, TREXIO_DELIM);
  }

  // H5Dvlen_reclaim is deprecated and replaced by H5Treclaim in HDF5 v.1.12.0
  #if (H5_VERS_MAJOR <= 1 && H5_VERS_MINOR < 12)
    status = H5Dvlen_reclaim(memtype, dspace, H5P_DEFAULT, rdata);
  #else
    status = H5Treclaim(memtype, dspace, H5P_DEFAULT, rdata);
  #endif

  if (status < 0) {
    FREE(rdata);
    H5Dclose(dset_id);
    H5Sclose(dspace);
    H5Tclose(memtype); 
    return TREXIO_FAILURE;
  }

  FREE(rdata); 
  H5Dclose(dset_id);
  H5Sclose(dspace);
  H5Tclose(memtype);

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_write_metadata_code_num (trexio_t* const file, const int64_t num)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* const f = (trexio_hdf5_t*) file;

  /* Write the dimensioning variables */
  const hid_t dtype = H5Tcopy(H5T_NATIVE_INT64);
  const hid_t dspace = H5Screate(H5S_SCALAR);
  
  const hid_t num_id = H5Acreate(f->metadata_group, METADATA_CODE_NUM_NAME, 
                                 dtype, dspace, H5P_DEFAULT, H5P_DEFAULT);
  if (num_id <= 0) {
    H5Sclose(dspace);
    H5Tclose(dtype);
    return TREXIO_INVALID_ID;
  }
  
  const herr_t status = H5Awrite(num_id, dtype, &(num));
  if (status < 0) {
    H5Aclose(num_id);
    H5Sclose(dspace);
    H5Tclose(dtype);
    return TREXIO_FAILURE;
  }
  
  H5Sclose(dspace);
  H5Aclose(num_id);
  H5Tclose(dtype);

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_write_metadata_author_num (trexio_t* const file, const int64_t num)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* const f = (trexio_hdf5_t*) file;

  /* Write the dimensioning variables */
  const hid_t dtype = H5Tcopy(H5T_NATIVE_INT64);
  const hid_t dspace = H5Screate(H5S_SCALAR);
  
  const hid_t num_id = H5Acreate(f->metadata_group, METADATA_AUTHOR_NUM_NAME, 
                                 dtype, dspace, H5P_DEFAULT, H5P_DEFAULT);
  if (num_id <= 0) {
    H5Sclose(dspace);
    H5Tclose(dtype);
    return TREXIO_INVALID_ID;
  }
  
  const herr_t status = H5Awrite(num_id, dtype, &(num));
  if (status < 0) {
    H5Aclose(num_id);
    H5Sclose(dspace);
    H5Tclose(dtype);
    return TREXIO_FAILURE;
  }
  
  H5Sclose(dspace);
  H5Aclose(num_id);
  H5Tclose(dtype);

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_write_electron_up_num (trexio_t* const file, const int64_t num)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* const f = (trexio_hdf5_t*) file;

  /* Write the dimensioning variables */
  const hid_t dtype = H5Tcopy(H5T_NATIVE_INT64);
  const hid_t dspace = H5Screate(H5S_SCALAR);
  
  const hid_t num_id = H5Acreate(f->electron_group, ELECTRON_UP_NUM_NAME, 
                                 dtype, dspace, H5P_DEFAULT, H5P_DEFAULT);
  if (num_id <= 0) {
    H5Sclose(dspace);
    H5Tclose(dtype);
    return TREXIO_INVALID_ID;
  }
  
  const herr_t status = H5Awrite(num_id, dtype, &(num));
  if (status < 0) {
    H5Aclose(num_id);
    H5Sclose(dspace);
    H5Tclose(dtype);
    return TREXIO_FAILURE;
  }
  
  H5Sclose(dspace);
  H5Aclose(num_id);
  H5Tclose(dtype);

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_write_electron_dn_num (trexio_t* const file, const int64_t num)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* const f = (trexio_hdf5_t*) file;

  /* Write the dimensioning variables */
  const hid_t dtype = H5Tcopy(H5T_NATIVE_INT64);
  const hid_t dspace = H5Screate(H5S_SCALAR);
  
  const hid_t num_id = H5Acreate(f->electron_group, ELECTRON_DN_NUM_NAME, 
                                 dtype, dspace, H5P_DEFAULT, H5P_DEFAULT);
  if (num_id <= 0) {
    H5Sclose(dspace);
    H5Tclose(dtype);
    return TREXIO_INVALID_ID;
  }
  
  const herr_t status = H5Awrite(num_id, dtype, &(num));
  if (status < 0) {
    H5Aclose(num_id);
    H5Sclose(dspace);
    H5Tclose(dtype);
    return TREXIO_FAILURE;
  }
  
  H5Sclose(dspace);
  H5Aclose(num_id);
  H5Tclose(dtype);

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_write_nucleus_num (trexio_t* const file, const int64_t num)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* const f = (trexio_hdf5_t*) file;

  /* Write the dimensioning variables */
  const hid_t dtype = H5Tcopy(H5T_NATIVE_INT64);
  const hid_t dspace = H5Screate(H5S_SCALAR);
  
  const hid_t num_id = H5Acreate(f->nucleus_group, NUCLEUS_NUM_NAME, 
                                 dtype, dspace, H5P_DEFAULT, H5P_DEFAULT);
  if (num_id <= 0) {
    H5Sclose(dspace);
    H5Tclose(dtype);
    return TREXIO_INVALID_ID;
  }
  
  const herr_t status = H5Awrite(num_id, dtype, &(num));
  if (status < 0) {
    H5Aclose(num_id);
    H5Sclose(dspace);
    H5Tclose(dtype);
    return TREXIO_FAILURE;
  }
  
  H5Sclose(dspace);
  H5Aclose(num_id);
  H5Tclose(dtype);

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_write_ecp_num (trexio_t* const file, const int64_t num)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* const f = (trexio_hdf5_t*) file;

  /* Write the dimensioning variables */
  const hid_t dtype = H5Tcopy(H5T_NATIVE_INT64);
  const hid_t dspace = H5Screate(H5S_SCALAR);
  
  const hid_t num_id = H5Acreate(f->ecp_group, ECP_NUM_NAME, 
                                 dtype, dspace, H5P_DEFAULT, H5P_DEFAULT);
  if (num_id <= 0) {
    H5Sclose(dspace);
    H5Tclose(dtype);
    return TREXIO_INVALID_ID;
  }
  
  const herr_t status = H5Awrite(num_id, dtype, &(num));
  if (status < 0) {
    H5Aclose(num_id);
    H5Sclose(dspace);
    H5Tclose(dtype);
    return TREXIO_FAILURE;
  }
  
  H5Sclose(dspace);
  H5Aclose(num_id);
  H5Tclose(dtype);

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_write_basis_prim_num (trexio_t* const file, const int64_t num)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* const f = (trexio_hdf5_t*) file;

  /* Write the dimensioning variables */
  const hid_t dtype = H5Tcopy(H5T_NATIVE_INT64);
  const hid_t dspace = H5Screate(H5S_SCALAR);
  
  const hid_t num_id = H5Acreate(f->basis_group, BASIS_PRIM_NUM_NAME, 
                                 dtype, dspace, H5P_DEFAULT, H5P_DEFAULT);
  if (num_id <= 0) {
    H5Sclose(dspace);
    H5Tclose(dtype);
    return TREXIO_INVALID_ID;
  }
  
  const herr_t status = H5Awrite(num_id, dtype, &(num));
  if (status < 0) {
    H5Aclose(num_id);
    H5Sclose(dspace);
    H5Tclose(dtype);
    return TREXIO_FAILURE;
  }
  
  H5Sclose(dspace);
  H5Aclose(num_id);
  H5Tclose(dtype);

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_write_basis_shell_num (trexio_t* const file, const int64_t num)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* const f = (trexio_hdf5_t*) file;

  /* Write the dimensioning variables */
  const hid_t dtype = H5Tcopy(H5T_NATIVE_INT64);
  const hid_t dspace = H5Screate(H5S_SCALAR);
  
  const hid_t num_id = H5Acreate(f->basis_group, BASIS_SHELL_NUM_NAME, 
                                 dtype, dspace, H5P_DEFAULT, H5P_DEFAULT);
  if (num_id <= 0) {
    H5Sclose(dspace);
    H5Tclose(dtype);
    return TREXIO_INVALID_ID;
  }
  
  const herr_t status = H5Awrite(num_id, dtype, &(num));
  if (status < 0) {
    H5Aclose(num_id);
    H5Sclose(dspace);
    H5Tclose(dtype);
    return TREXIO_FAILURE;
  }
  
  H5Sclose(dspace);
  H5Aclose(num_id);
  H5Tclose(dtype);

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_write_ao_cartesian (trexio_t* const file, const int64_t num)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* const f = (trexio_hdf5_t*) file;

  /* Write the dimensioning variables */
  const hid_t dtype = H5Tcopy(H5T_NATIVE_INT64);
  const hid_t dspace = H5Screate(H5S_SCALAR);
  
  const hid_t num_id = H5Acreate(f->ao_group, AO_CARTESIAN_NAME, 
                                 dtype, dspace, H5P_DEFAULT, H5P_DEFAULT);
  if (num_id <= 0) {
    H5Sclose(dspace);
    H5Tclose(dtype);
    return TREXIO_INVALID_ID;
  }
  
  const herr_t status = H5Awrite(num_id, dtype, &(num));
  if (status < 0) {
    H5Aclose(num_id);
    H5Sclose(dspace);
    H5Tclose(dtype);
    return TREXIO_FAILURE;
  }
  
  H5Sclose(dspace);
  H5Aclose(num_id);
  H5Tclose(dtype);

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_write_ao_num (trexio_t* const file, const int64_t num)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* const f = (trexio_hdf5_t*) file;

  /* Write the dimensioning variables */
  const hid_t dtype = H5Tcopy(H5T_NATIVE_INT64);
  const hid_t dspace = H5Screate(H5S_SCALAR);
  
  const hid_t num_id = H5Acreate(f->ao_group, AO_NUM_NAME, 
                                 dtype, dspace, H5P_DEFAULT, H5P_DEFAULT);
  if (num_id <= 0) {
    H5Sclose(dspace);
    H5Tclose(dtype);
    return TREXIO_INVALID_ID;
  }
  
  const herr_t status = H5Awrite(num_id, dtype, &(num));
  if (status < 0) {
    H5Aclose(num_id);
    H5Sclose(dspace);
    H5Tclose(dtype);
    return TREXIO_FAILURE;
  }
  
  H5Sclose(dspace);
  H5Aclose(num_id);
  H5Tclose(dtype);

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_write_mo_num (trexio_t* const file, const int64_t num)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;

  trexio_hdf5_t* const f = (trexio_hdf5_t*) file;

  /* Write the dimensioning variables */
  const hid_t dtype = H5Tcopy(H5T_NATIVE_INT64);
  const hid_t dspace = H5Screate(H5S_SCALAR);
  
  const hid_t num_id = H5Acreate(f->mo_group, MO_NUM_NAME, 
                                 dtype, dspace, H5P_DEFAULT, H5P_DEFAULT);
  if (num_id <= 0) {
    H5Sclose(dspace);
    H5Tclose(dtype);
    return TREXIO_INVALID_ID;
  }
  
  const herr_t status = H5Awrite(num_id, dtype, &(num));
  if (status < 0) {
    H5Aclose(num_id);
    H5Sclose(dspace);
    H5Tclose(dtype);
    return TREXIO_FAILURE;
  }
  
  H5Sclose(dspace);
  H5Aclose(num_id);
  H5Tclose(dtype);

  return TREXIO_SUCCESS;
}

trexio_exit_code
trexio_hdf5_write_metadata_package_version (trexio_t* const file, const char* str)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (str  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* const f = (trexio_hdf5_t*) file;


  /* Setup the dataspace */
  const hid_t dtype_id = H5Tcopy(H5T_C_S1);
  if (dtype_id <= 0) return TREXIO_INVALID_ID;

  size_t str_attr_len = strlen(str) + 1;

  herr_t status;
  status = H5Tset_size(dtype_id, str_attr_len);
  if (status < 0) return TREXIO_FAILURE;

  status = H5Tset_strpad(dtype_id, H5T_STR_NULLTERM);
  if (status < 0) return TREXIO_FAILURE;

  const hid_t dspace_id = H5Screate(H5S_SCALAR);
  if (dspace_id <= 0) return TREXIO_INVALID_ID;
  
  /* Create the metadata_package_version attribute of metadata group */
  const hid_t str_id = H5Acreate(f->metadata_group, METADATA_PACKAGE_VERSION_NAME, dtype_id, dspace_id,
                       H5P_DEFAULT, H5P_DEFAULT);

  if (str_id <= 0) {
    H5Sclose(dspace_id);
    H5Tclose(dtype_id);
    return TREXIO_INVALID_ID;
  }
  
  status = H5Awrite(str_id, dtype_id, str);
  if (status < 0) {
    H5Aclose(str_id);
    H5Sclose(dspace_id);
    H5Tclose(dtype_id);
    return TREXIO_FAILURE;
  }
  
  H5Aclose(str_id);
  H5Sclose(dspace_id);
  H5Tclose(dtype_id);
  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_metadata_description (trexio_t* const file, const char* str)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (str  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* const f = (trexio_hdf5_t*) file;


  /* Setup the dataspace */
  const hid_t dtype_id = H5Tcopy(H5T_C_S1);
  if (dtype_id <= 0) return TREXIO_INVALID_ID;

  size_t str_attr_len = strlen(str) + 1;

  herr_t status;
  status = H5Tset_size(dtype_id, str_attr_len);
  if (status < 0) return TREXIO_FAILURE;

  status = H5Tset_strpad(dtype_id, H5T_STR_NULLTERM);
  if (status < 0) return TREXIO_FAILURE;

  const hid_t dspace_id = H5Screate(H5S_SCALAR);
  if (dspace_id <= 0) return TREXIO_INVALID_ID;
  
  /* Create the metadata_description attribute of metadata group */
  const hid_t str_id = H5Acreate(f->metadata_group, METADATA_DESCRIPTION_NAME, dtype_id, dspace_id,
                       H5P_DEFAULT, H5P_DEFAULT);

  if (str_id <= 0) {
    H5Sclose(dspace_id);
    H5Tclose(dtype_id);
    return TREXIO_INVALID_ID;
  }
  
  status = H5Awrite(str_id, dtype_id, str);
  if (status < 0) {
    H5Aclose(str_id);
    H5Sclose(dspace_id);
    H5Tclose(dtype_id);
    return TREXIO_FAILURE;
  }
  
  H5Aclose(str_id);
  H5Sclose(dspace_id);
  H5Tclose(dtype_id);
  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_nucleus_point_group (trexio_t* const file, const char* str)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (str  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* const f = (trexio_hdf5_t*) file;


  /* Setup the dataspace */
  const hid_t dtype_id = H5Tcopy(H5T_C_S1);
  if (dtype_id <= 0) return TREXIO_INVALID_ID;

  size_t str_attr_len = strlen(str) + 1;

  herr_t status;
  status = H5Tset_size(dtype_id, str_attr_len);
  if (status < 0) return TREXIO_FAILURE;

  status = H5Tset_strpad(dtype_id, H5T_STR_NULLTERM);
  if (status < 0) return TREXIO_FAILURE;

  const hid_t dspace_id = H5Screate(H5S_SCALAR);
  if (dspace_id <= 0) return TREXIO_INVALID_ID;
  
  /* Create the nucleus_point_group attribute of nucleus group */
  const hid_t str_id = H5Acreate(f->nucleus_group, NUCLEUS_POINT_GROUP_NAME, dtype_id, dspace_id,
                       H5P_DEFAULT, H5P_DEFAULT);

  if (str_id <= 0) {
    H5Sclose(dspace_id);
    H5Tclose(dtype_id);
    return TREXIO_INVALID_ID;
  }
  
  status = H5Awrite(str_id, dtype_id, str);
  if (status < 0) {
    H5Aclose(str_id);
    H5Sclose(dspace_id);
    H5Tclose(dtype_id);
    return TREXIO_FAILURE;
  }
  
  H5Aclose(str_id);
  H5Sclose(dspace_id);
  H5Tclose(dtype_id);
  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_basis_type (trexio_t* const file, const char* str)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (str  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* const f = (trexio_hdf5_t*) file;


  /* Setup the dataspace */
  const hid_t dtype_id = H5Tcopy(H5T_C_S1);
  if (dtype_id <= 0) return TREXIO_INVALID_ID;

  size_t str_attr_len = strlen(str) + 1;

  herr_t status;
  status = H5Tset_size(dtype_id, str_attr_len);
  if (status < 0) return TREXIO_FAILURE;

  status = H5Tset_strpad(dtype_id, H5T_STR_NULLTERM);
  if (status < 0) return TREXIO_FAILURE;

  const hid_t dspace_id = H5Screate(H5S_SCALAR);
  if (dspace_id <= 0) return TREXIO_INVALID_ID;
  
  /* Create the basis_type attribute of basis group */
  const hid_t str_id = H5Acreate(f->basis_group, BASIS_TYPE_NAME, dtype_id, dspace_id,
                       H5P_DEFAULT, H5P_DEFAULT);

  if (str_id <= 0) {
    H5Sclose(dspace_id);
    H5Tclose(dtype_id);
    return TREXIO_INVALID_ID;
  }
  
  status = H5Awrite(str_id, dtype_id, str);
  if (status < 0) {
    H5Aclose(str_id);
    H5Sclose(dspace_id);
    H5Tclose(dtype_id);
    return TREXIO_FAILURE;
  }
  
  H5Aclose(str_id);
  H5Sclose(dspace_id);
  H5Tclose(dtype_id);
  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_mo_type (trexio_t* const file, const char* str)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (str  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* const f = (trexio_hdf5_t*) file;


  /* Setup the dataspace */
  const hid_t dtype_id = H5Tcopy(H5T_C_S1);
  if (dtype_id <= 0) return TREXIO_INVALID_ID;

  size_t str_attr_len = strlen(str) + 1;

  herr_t status;
  status = H5Tset_size(dtype_id, str_attr_len);
  if (status < 0) return TREXIO_FAILURE;

  status = H5Tset_strpad(dtype_id, H5T_STR_NULLTERM);
  if (status < 0) return TREXIO_FAILURE;

  const hid_t dspace_id = H5Screate(H5S_SCALAR);
  if (dspace_id <= 0) return TREXIO_INVALID_ID;
  
  /* Create the mo_type attribute of mo group */
  const hid_t str_id = H5Acreate(f->mo_group, MO_TYPE_NAME, dtype_id, dspace_id,
                       H5P_DEFAULT, H5P_DEFAULT);

  if (str_id <= 0) {
    H5Sclose(dspace_id);
    H5Tclose(dtype_id);
    return TREXIO_INVALID_ID;
  }
  
  status = H5Awrite(str_id, dtype_id, str);
  if (status < 0) {
    H5Aclose(str_id);
    H5Sclose(dspace_id);
    H5Tclose(dtype_id);
    return TREXIO_FAILURE;
  }
  
  H5Aclose(str_id);
  H5Sclose(dspace_id);
  H5Tclose(dtype_id);
  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_nucleus_charge (trexio_t* const file, const double* nucleus_charge, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (nucleus_charge  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->nucleus_group, NUCLEUS_CHARGE_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->nucleus_group,
					   NUCLEUS_CHARGE_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   nucleus_charge);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->nucleus_group, NUCLEUS_CHARGE_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   nucleus_charge);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_nucleus_coord (trexio_t* const file, const double* nucleus_coord, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (nucleus_coord  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->nucleus_group, NUCLEUS_COORD_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->nucleus_group,
					   NUCLEUS_COORD_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   nucleus_coord);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->nucleus_group, NUCLEUS_COORD_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   nucleus_coord);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_ecp_max_ang_mom_plus_1 (trexio_t* const file, const int64_t* ecp_max_ang_mom_plus_1, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ecp_max_ang_mom_plus_1  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->ecp_group, ECP_MAX_ANG_MOM_PLUS_1_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->ecp_group,
					   ECP_MAX_ANG_MOM_PLUS_1_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_INT64,
					   ecp_max_ang_mom_plus_1);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->ecp_group, ECP_MAX_ANG_MOM_PLUS_1_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_INT64,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   ecp_max_ang_mom_plus_1);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_ecp_z_core (trexio_t* const file, const int64_t* ecp_z_core, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ecp_z_core  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->ecp_group, ECP_Z_CORE_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->ecp_group,
					   ECP_Z_CORE_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_INT64,
					   ecp_z_core);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->ecp_group, ECP_Z_CORE_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_INT64,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   ecp_z_core);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_ecp_ang_mom (trexio_t* const file, const int64_t* ecp_ang_mom, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ecp_ang_mom  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->ecp_group, ECP_ANG_MOM_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->ecp_group,
					   ECP_ANG_MOM_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_INT64,
					   ecp_ang_mom);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->ecp_group, ECP_ANG_MOM_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_INT64,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   ecp_ang_mom);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_ecp_nucleus_index (trexio_t* const file, const int64_t* ecp_nucleus_index, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ecp_nucleus_index  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->ecp_group, ECP_NUCLEUS_INDEX_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->ecp_group,
					   ECP_NUCLEUS_INDEX_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_INT64,
					   ecp_nucleus_index);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->ecp_group, ECP_NUCLEUS_INDEX_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_INT64,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   ecp_nucleus_index);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_ecp_exponent (trexio_t* const file, const double* ecp_exponent, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ecp_exponent  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->ecp_group, ECP_EXPONENT_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->ecp_group,
					   ECP_EXPONENT_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   ecp_exponent);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->ecp_group, ECP_EXPONENT_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   ecp_exponent);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_ecp_coefficient (trexio_t* const file, const double* ecp_coefficient, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ecp_coefficient  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->ecp_group, ECP_COEFFICIENT_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->ecp_group,
					   ECP_COEFFICIENT_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   ecp_coefficient);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->ecp_group, ECP_COEFFICIENT_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   ecp_coefficient);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_ecp_power (trexio_t* const file, const int64_t* ecp_power, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ecp_power  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->ecp_group, ECP_POWER_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->ecp_group,
					   ECP_POWER_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_INT64,
					   ecp_power);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->ecp_group, ECP_POWER_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_INT64,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   ecp_power);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_basis_nucleus_index (trexio_t* const file, const int64_t* basis_nucleus_index, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (basis_nucleus_index  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->basis_group, BASIS_NUCLEUS_INDEX_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->basis_group,
					   BASIS_NUCLEUS_INDEX_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_INT64,
					   basis_nucleus_index);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->basis_group, BASIS_NUCLEUS_INDEX_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_INT64,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   basis_nucleus_index);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_basis_shell_ang_mom (trexio_t* const file, const int64_t* basis_shell_ang_mom, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (basis_shell_ang_mom  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->basis_group, BASIS_SHELL_ANG_MOM_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->basis_group,
					   BASIS_SHELL_ANG_MOM_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_INT64,
					   basis_shell_ang_mom);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->basis_group, BASIS_SHELL_ANG_MOM_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_INT64,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   basis_shell_ang_mom);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_basis_shell_factor (trexio_t* const file, const double* basis_shell_factor, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (basis_shell_factor  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->basis_group, BASIS_SHELL_FACTOR_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->basis_group,
					   BASIS_SHELL_FACTOR_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   basis_shell_factor);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->basis_group, BASIS_SHELL_FACTOR_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   basis_shell_factor);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_basis_shell_index (trexio_t* const file, const int64_t* basis_shell_index, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (basis_shell_index  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->basis_group, BASIS_SHELL_INDEX_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->basis_group,
					   BASIS_SHELL_INDEX_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_INT64,
					   basis_shell_index);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->basis_group, BASIS_SHELL_INDEX_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_INT64,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   basis_shell_index);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_basis_exponent (trexio_t* const file, const double* basis_exponent, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (basis_exponent  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->basis_group, BASIS_EXPONENT_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->basis_group,
					   BASIS_EXPONENT_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   basis_exponent);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->basis_group, BASIS_EXPONENT_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   basis_exponent);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_basis_coefficient (trexio_t* const file, const double* basis_coefficient, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (basis_coefficient  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->basis_group, BASIS_COEFFICIENT_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->basis_group,
					   BASIS_COEFFICIENT_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   basis_coefficient);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->basis_group, BASIS_COEFFICIENT_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   basis_coefficient);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_basis_prim_factor (trexio_t* const file, const double* basis_prim_factor, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (basis_prim_factor  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->basis_group, BASIS_PRIM_FACTOR_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->basis_group,
					   BASIS_PRIM_FACTOR_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   basis_prim_factor);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->basis_group, BASIS_PRIM_FACTOR_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   basis_prim_factor);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_ao_shell (trexio_t* const file, const int64_t* ao_shell, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ao_shell  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->ao_group, AO_SHELL_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->ao_group,
					   AO_SHELL_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_INT64,
					   ao_shell);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->ao_group, AO_SHELL_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_INT64,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   ao_shell);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_ao_normalization (trexio_t* const file, const double* ao_normalization, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ao_normalization  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->ao_group, AO_NORMALIZATION_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->ao_group,
					   AO_NORMALIZATION_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   ao_normalization);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->ao_group, AO_NORMALIZATION_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   ao_normalization);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_ao_1e_int_overlap (trexio_t* const file, const double* ao_1e_int_overlap, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ao_1e_int_overlap  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->ao_1e_int_group, AO_1E_INT_OVERLAP_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->ao_1e_int_group,
					   AO_1E_INT_OVERLAP_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   ao_1e_int_overlap);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->ao_1e_int_group, AO_1E_INT_OVERLAP_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   ao_1e_int_overlap);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_ao_1e_int_kinetic (trexio_t* const file, const double* ao_1e_int_kinetic, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ao_1e_int_kinetic  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->ao_1e_int_group, AO_1E_INT_KINETIC_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->ao_1e_int_group,
					   AO_1E_INT_KINETIC_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   ao_1e_int_kinetic);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->ao_1e_int_group, AO_1E_INT_KINETIC_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   ao_1e_int_kinetic);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_ao_1e_int_potential_n_e (trexio_t* const file, const double* ao_1e_int_potential_n_e, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ao_1e_int_potential_n_e  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->ao_1e_int_group, AO_1E_INT_POTENTIAL_N_E_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->ao_1e_int_group,
					   AO_1E_INT_POTENTIAL_N_E_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   ao_1e_int_potential_n_e);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->ao_1e_int_group, AO_1E_INT_POTENTIAL_N_E_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   ao_1e_int_potential_n_e);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_ao_1e_int_ecp_local (trexio_t* const file, const double* ao_1e_int_ecp_local, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ao_1e_int_ecp_local  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->ao_1e_int_group, AO_1E_INT_ECP_LOCAL_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->ao_1e_int_group,
					   AO_1E_INT_ECP_LOCAL_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   ao_1e_int_ecp_local);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->ao_1e_int_group, AO_1E_INT_ECP_LOCAL_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   ao_1e_int_ecp_local);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_ao_1e_int_ecp_non_local (trexio_t* const file, const double* ao_1e_int_ecp_non_local, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ao_1e_int_ecp_non_local  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->ao_1e_int_group, AO_1E_INT_ECP_NON_LOCAL_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->ao_1e_int_group,
					   AO_1E_INT_ECP_NON_LOCAL_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   ao_1e_int_ecp_non_local);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->ao_1e_int_group, AO_1E_INT_ECP_NON_LOCAL_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   ao_1e_int_ecp_non_local);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_ao_1e_int_core_hamiltonian (trexio_t* const file, const double* ao_1e_int_core_hamiltonian, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ao_1e_int_core_hamiltonian  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->ao_1e_int_group, AO_1E_INT_CORE_HAMILTONIAN_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->ao_1e_int_group,
					   AO_1E_INT_CORE_HAMILTONIAN_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   ao_1e_int_core_hamiltonian);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->ao_1e_int_group, AO_1E_INT_CORE_HAMILTONIAN_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   ao_1e_int_core_hamiltonian);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_ao_2e_int_eri (trexio_t* const file, const double* ao_2e_int_eri, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ao_2e_int_eri  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->ao_2e_int_group, AO_2E_INT_ERI_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->ao_2e_int_group,
					   AO_2E_INT_ERI_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   ao_2e_int_eri);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->ao_2e_int_group, AO_2E_INT_ERI_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   ao_2e_int_eri);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_ao_2e_int_eri_lr (trexio_t* const file, const double* ao_2e_int_eri_lr, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (ao_2e_int_eri_lr  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->ao_2e_int_group, AO_2E_INT_ERI_LR_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->ao_2e_int_group,
					   AO_2E_INT_ERI_LR_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   ao_2e_int_eri_lr);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->ao_2e_int_group, AO_2E_INT_ERI_LR_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   ao_2e_int_eri_lr);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_mo_coefficient (trexio_t* const file, const double* mo_coefficient, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_coefficient  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->mo_group, MO_COEFFICIENT_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->mo_group,
					   MO_COEFFICIENT_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   mo_coefficient);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->mo_group, MO_COEFFICIENT_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   mo_coefficient);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_mo_occupation (trexio_t* const file, const double* mo_occupation, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_occupation  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->mo_group, MO_OCCUPATION_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->mo_group,
					   MO_OCCUPATION_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   mo_occupation);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->mo_group, MO_OCCUPATION_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   mo_occupation);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_mo_1e_int_overlap (trexio_t* const file, const double* mo_1e_int_overlap, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_1e_int_overlap  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->mo_1e_int_group, MO_1E_INT_OVERLAP_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->mo_1e_int_group,
					   MO_1E_INT_OVERLAP_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   mo_1e_int_overlap);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->mo_1e_int_group, MO_1E_INT_OVERLAP_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   mo_1e_int_overlap);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_mo_1e_int_kinetic (trexio_t* const file, const double* mo_1e_int_kinetic, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_1e_int_kinetic  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->mo_1e_int_group, MO_1E_INT_KINETIC_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->mo_1e_int_group,
					   MO_1E_INT_KINETIC_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   mo_1e_int_kinetic);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->mo_1e_int_group, MO_1E_INT_KINETIC_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   mo_1e_int_kinetic);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_mo_1e_int_potential_n_e (trexio_t* const file, const double* mo_1e_int_potential_n_e, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_1e_int_potential_n_e  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->mo_1e_int_group, MO_1E_INT_POTENTIAL_N_E_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->mo_1e_int_group,
					   MO_1E_INT_POTENTIAL_N_E_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   mo_1e_int_potential_n_e);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->mo_1e_int_group, MO_1E_INT_POTENTIAL_N_E_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   mo_1e_int_potential_n_e);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_mo_1e_int_ecp_local (trexio_t* const file, const double* mo_1e_int_ecp_local, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_1e_int_ecp_local  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->mo_1e_int_group, MO_1E_INT_ECP_LOCAL_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->mo_1e_int_group,
					   MO_1E_INT_ECP_LOCAL_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   mo_1e_int_ecp_local);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->mo_1e_int_group, MO_1E_INT_ECP_LOCAL_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   mo_1e_int_ecp_local);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_mo_1e_int_ecp_non_local (trexio_t* const file, const double* mo_1e_int_ecp_non_local, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_1e_int_ecp_non_local  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->mo_1e_int_group, MO_1E_INT_ECP_NON_LOCAL_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->mo_1e_int_group,
					   MO_1E_INT_ECP_NON_LOCAL_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   mo_1e_int_ecp_non_local);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->mo_1e_int_group, MO_1E_INT_ECP_NON_LOCAL_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   mo_1e_int_ecp_non_local);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_mo_1e_int_core_hamiltonian (trexio_t* const file, const double* mo_1e_int_core_hamiltonian, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_1e_int_core_hamiltonian  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->mo_1e_int_group, MO_1E_INT_CORE_HAMILTONIAN_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->mo_1e_int_group,
					   MO_1E_INT_CORE_HAMILTONIAN_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   mo_1e_int_core_hamiltonian);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->mo_1e_int_group, MO_1E_INT_CORE_HAMILTONIAN_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   mo_1e_int_core_hamiltonian);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_mo_2e_int_eri (trexio_t* const file, const double* mo_2e_int_eri, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_2e_int_eri  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->mo_2e_int_group, MO_2E_INT_ERI_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->mo_2e_int_group,
					   MO_2E_INT_ERI_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   mo_2e_int_eri);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->mo_2e_int_group, MO_2E_INT_ERI_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   mo_2e_int_eri);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_mo_2e_int_eri_lr (trexio_t* const file, const double* mo_2e_int_eri_lr, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_2e_int_eri_lr  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  if ( H5LTfind_dataset(f->mo_2e_int_group, MO_2E_INT_ERI_LR_NAME) != 1 ) {

    const herr_t status = H5LTmake_dataset(f->mo_2e_int_group,
					   MO_2E_INT_ERI_LR_NAME,
					   (int) rank, (const hsize_t*) dims,
					   H5T_NATIVE_DOUBLE,
					   mo_2e_int_eri_lr);
    if (status < 0) return TREXIO_FAILURE;

  } else {

    hid_t dset_id = H5Dopen(f->mo_2e_int_group, MO_2E_INT_ERI_LR_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    const herr_t status = H5Dwrite(dset_id,
				   H5T_NATIVE_DOUBLE,
				   H5S_ALL, H5S_ALL, H5P_DEFAULT,
				   mo_2e_int_eri_lr);

    H5Dclose(dset_id);
    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_metadata_code (trexio_t* const file, const char** metadata_code, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (metadata_code  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status;
  hid_t dset_id;

  /* we are going to write variable-length strings */
  hid_t memtype = H5Tcopy (H5T_C_S1);
  if (memtype <= 0) return TREXIO_INVALID_ID;

  status = H5Tset_size (memtype, H5T_VARIABLE);
  if (status < 0) return TREXIO_FAILURE;

  if ( H5LTfind_dataset(f->metadata_group, METADATA_CODE_NAME) != 1 ) {

    /* code to create dataset */   
    hid_t filetype = H5Tcopy (H5T_FORTRAN_S1);
    if (filetype <= 0) return TREXIO_INVALID_ID;

    status = H5Tset_size (filetype, H5T_VARIABLE);
    if (status < 0) return TREXIO_FAILURE;

    hid_t dspace = H5Screate_simple( (int) rank, (const hsize_t*) dims, NULL);
    if (dspace <= 0) return TREXIO_INVALID_ID;

    dset_id = H5Dcreate (f->metadata_group, METADATA_CODE_NAME, filetype, dspace,
                         H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    status = H5Dwrite (dset_id, memtype,
                       H5S_ALL, H5S_ALL, H5P_DEFAULT,
                       metadata_code);

    H5Dclose (dset_id);
    H5Sclose (dspace);
    H5Tclose (filetype);
    H5Tclose (memtype);

    if (status < 0) return TREXIO_FAILURE;

  } else {

    dset_id = H5Dopen(f->metadata_group, METADATA_CODE_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    /* code to write dataset */
    status = H5Dwrite(dset_id, memtype,
		      H5S_ALL, H5S_ALL, H5P_DEFAULT,
		      metadata_code);

    H5Dclose(dset_id);
    H5Tclose(memtype);

    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_metadata_author (trexio_t* const file, const char** metadata_author, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (metadata_author  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status;
  hid_t dset_id;

  /* we are going to write variable-length strings */
  hid_t memtype = H5Tcopy (H5T_C_S1);
  if (memtype <= 0) return TREXIO_INVALID_ID;

  status = H5Tset_size (memtype, H5T_VARIABLE);
  if (status < 0) return TREXIO_FAILURE;

  if ( H5LTfind_dataset(f->metadata_group, METADATA_AUTHOR_NAME) != 1 ) {

    /* code to create dataset */   
    hid_t filetype = H5Tcopy (H5T_FORTRAN_S1);
    if (filetype <= 0) return TREXIO_INVALID_ID;

    status = H5Tset_size (filetype, H5T_VARIABLE);
    if (status < 0) return TREXIO_FAILURE;

    hid_t dspace = H5Screate_simple( (int) rank, (const hsize_t*) dims, NULL);
    if (dspace <= 0) return TREXIO_INVALID_ID;

    dset_id = H5Dcreate (f->metadata_group, METADATA_AUTHOR_NAME, filetype, dspace,
                         H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    status = H5Dwrite (dset_id, memtype,
                       H5S_ALL, H5S_ALL, H5P_DEFAULT,
                       metadata_author);

    H5Dclose (dset_id);
    H5Sclose (dspace);
    H5Tclose (filetype);
    H5Tclose (memtype);

    if (status < 0) return TREXIO_FAILURE;

  } else {

    dset_id = H5Dopen(f->metadata_group, METADATA_AUTHOR_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    /* code to write dataset */
    status = H5Dwrite(dset_id, memtype,
		      H5S_ALL, H5S_ALL, H5P_DEFAULT,
		      metadata_author);

    H5Dclose(dset_id);
    H5Tclose(memtype);

    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_nucleus_label (trexio_t* const file, const char** nucleus_label, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (nucleus_label  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status;
  hid_t dset_id;

  /* we are going to write variable-length strings */
  hid_t memtype = H5Tcopy (H5T_C_S1);
  if (memtype <= 0) return TREXIO_INVALID_ID;

  status = H5Tset_size (memtype, H5T_VARIABLE);
  if (status < 0) return TREXIO_FAILURE;

  if ( H5LTfind_dataset(f->nucleus_group, NUCLEUS_LABEL_NAME) != 1 ) {

    /* code to create dataset */   
    hid_t filetype = H5Tcopy (H5T_FORTRAN_S1);
    if (filetype <= 0) return TREXIO_INVALID_ID;

    status = H5Tset_size (filetype, H5T_VARIABLE);
    if (status < 0) return TREXIO_FAILURE;

    hid_t dspace = H5Screate_simple( (int) rank, (const hsize_t*) dims, NULL);
    if (dspace <= 0) return TREXIO_INVALID_ID;

    dset_id = H5Dcreate (f->nucleus_group, NUCLEUS_LABEL_NAME, filetype, dspace,
                         H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    status = H5Dwrite (dset_id, memtype,
                       H5S_ALL, H5S_ALL, H5P_DEFAULT,
                       nucleus_label);

    H5Dclose (dset_id);
    H5Sclose (dspace);
    H5Tclose (filetype);
    H5Tclose (memtype);

    if (status < 0) return TREXIO_FAILURE;

  } else {

    dset_id = H5Dopen(f->nucleus_group, NUCLEUS_LABEL_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    /* code to write dataset */
    status = H5Dwrite(dset_id, memtype,
		      H5S_ALL, H5S_ALL, H5P_DEFAULT,
		      nucleus_label);

    H5Dclose(dset_id);
    H5Tclose(memtype);

    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_mo_class (trexio_t* const file, const char** mo_class, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_class  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status;
  hid_t dset_id;

  /* we are going to write variable-length strings */
  hid_t memtype = H5Tcopy (H5T_C_S1);
  if (memtype <= 0) return TREXIO_INVALID_ID;

  status = H5Tset_size (memtype, H5T_VARIABLE);
  if (status < 0) return TREXIO_FAILURE;

  if ( H5LTfind_dataset(f->mo_group, MO_CLASS_NAME) != 1 ) {

    /* code to create dataset */   
    hid_t filetype = H5Tcopy (H5T_FORTRAN_S1);
    if (filetype <= 0) return TREXIO_INVALID_ID;

    status = H5Tset_size (filetype, H5T_VARIABLE);
    if (status < 0) return TREXIO_FAILURE;

    hid_t dspace = H5Screate_simple( (int) rank, (const hsize_t*) dims, NULL);
    if (dspace <= 0) return TREXIO_INVALID_ID;

    dset_id = H5Dcreate (f->mo_group, MO_CLASS_NAME, filetype, dspace,
                         H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    status = H5Dwrite (dset_id, memtype,
                       H5S_ALL, H5S_ALL, H5P_DEFAULT,
                       mo_class);

    H5Dclose (dset_id);
    H5Sclose (dspace);
    H5Tclose (filetype);
    H5Tclose (memtype);

    if (status < 0) return TREXIO_FAILURE;

  } else {

    dset_id = H5Dopen(f->mo_group, MO_CLASS_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    /* code to write dataset */
    status = H5Dwrite(dset_id, memtype,
		      H5S_ALL, H5S_ALL, H5P_DEFAULT,
		      mo_class);

    H5Dclose(dset_id);
    H5Tclose(memtype);

    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

trexio_exit_code
trexio_hdf5_write_mo_symmetry (trexio_t* const file, const char** mo_symmetry, const uint32_t rank, const uint64_t* dims)
{

  if (file == NULL) return TREXIO_INVALID_ARG_1;
  if (mo_symmetry  == NULL) return TREXIO_INVALID_ARG_2;

  trexio_hdf5_t* f = (trexio_hdf5_t*) file;

  herr_t status;
  hid_t dset_id;

  /* we are going to write variable-length strings */
  hid_t memtype = H5Tcopy (H5T_C_S1);
  if (memtype <= 0) return TREXIO_INVALID_ID;

  status = H5Tset_size (memtype, H5T_VARIABLE);
  if (status < 0) return TREXIO_FAILURE;

  if ( H5LTfind_dataset(f->mo_group, MO_SYMMETRY_NAME) != 1 ) {

    /* code to create dataset */   
    hid_t filetype = H5Tcopy (H5T_FORTRAN_S1);
    if (filetype <= 0) return TREXIO_INVALID_ID;

    status = H5Tset_size (filetype, H5T_VARIABLE);
    if (status < 0) return TREXIO_FAILURE;

    hid_t dspace = H5Screate_simple( (int) rank, (const hsize_t*) dims, NULL);
    if (dspace <= 0) return TREXIO_INVALID_ID;

    dset_id = H5Dcreate (f->mo_group, MO_SYMMETRY_NAME, filetype, dspace,
                         H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    status = H5Dwrite (dset_id, memtype,
                       H5S_ALL, H5S_ALL, H5P_DEFAULT,
                       mo_symmetry);

    H5Dclose (dset_id);
    H5Sclose (dspace);
    H5Tclose (filetype);
    H5Tclose (memtype);

    if (status < 0) return TREXIO_FAILURE;

  } else {

    dset_id = H5Dopen(f->mo_group, MO_SYMMETRY_NAME, H5P_DEFAULT);
    if (dset_id <= 0) return TREXIO_INVALID_ID;

    /* code to write dataset */
    status = H5Dwrite(dset_id, memtype,
		      H5S_ALL, H5S_ALL, H5P_DEFAULT,
		      mo_symmetry);

    H5Dclose(dset_id);
    H5Tclose(memtype);

    if (status < 0) return TREXIO_FAILURE;

  }

  return TREXIO_SUCCESS;

}

