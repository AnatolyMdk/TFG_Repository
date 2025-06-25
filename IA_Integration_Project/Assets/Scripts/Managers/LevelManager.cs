using UnityEngine;
using UnityEngine.SceneManagement;

public class LevelManager : MonoBehaviour
{
    public static LevelManager Instance;

    public int currentLevel = 1;

    void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else if (Instance != this)
        {
            Destroy(gameObject);
        }
    }


    public void LoadNextLevel()
    {
        currentLevel++;
        string nextSceneName = "Level" + currentLevel;
        Debug.Log("Cargando escena: " + nextSceneName);
        SceneManager.LoadScene(nextSceneName);
    }

    public void LoadLevel(int level)
    {
        currentLevel = level;
        string sceneName = "Level" + currentLevel;
        Debug.Log("Cargando escena: " + sceneName);
        SceneManager.LoadScene(sceneName);
    }
}
