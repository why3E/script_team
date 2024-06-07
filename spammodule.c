#include "C:\Program Files\Python312\include\python.h"

// 리스트를 받아 정렬하는 함수
static PyObject*
spam_sort(PyObject* self, PyObject* args)
{
    PyObject* listObj;
    int descending;

    // 리스트 객체와 bool 값을 파싱합니다.
    if (!PyArg_ParseTuple(args, "O!p", &PyList_Type, &listObj, &descending))
        return NULL;

    // 리스트의 길이를 가져옵니다.
    Py_ssize_t len = PyList_Size(listObj);
    if (len < 0)
        return NULL;

    // 리스트를 복사하여 정렬합니다.
    PyObject* sortedList = PyList_GetSlice(listObj, 0, len);
    if (sortedList == NULL)
        return NULL;

    // 오름차순으로 정렬합니다.
    if (PyList_Sort(sortedList) != 0) {
        Py_DECREF(sortedList);
        return NULL;
    }

    // 만약 내림차순이라면 리스트를 뒤집습니다.
    if (descending) {
        if (PyList_Reverse(sortedList) != 0) {
            Py_DECREF(sortedList);
            return NULL;
        }
    }

    return sortedList; // 정렬된 리스트를 반환합니다.
}

static PyMethodDef SpamMethods[] = {
    { "sort", spam_sort, METH_VARARGS, "Sort a list. Pass True for descending order and False for ascending order." },
    { NULL, NULL, 0, NULL } // 배열의 끝을 나타냅니다.
};

static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "spam",               // 모듈 이름
    "It is test module.", // 모듈 설명을 적는 부분, 모듈의 __doc__에 저장됩니다.
    -1,SpamMethods
};

PyMODINIT_FUNC
PyInit_spam(void)
{
    return PyModule_Create(&spammodule);
}
