using System.Collections;
using System.Text;
using UnityEngine;
using UnityEngine.Networking;
using TMPro;
using UnityEngine.UI;

[System.Serializable]
public class Message
{
    public string npc;      // Nombre del NPC actual
    public string entrada;  // Mensaje del jugador
}

[System.Serializable]
public class ChatResponse
{
    public string response;
}

public class ChatMessage : MonoBehaviour
{
    [Header("UI References")]
    public TMP_InputField inputField;
    public TMP_Text chatText;
    public Button sendButton;

    [Header("API Settings")]
    [SerializeField] private string apiUrl = "http://127.0.0.1:5000/chat";

    private string currentNpcName = "NPC";

    void Start()
    {
        if (sendButton != null)
            sendButton.onClick.AddListener(OnSendButtonClicked);
        else
            Debug.LogWarning("Send Button no asignado en ChatMessage.");
    }

    public void SetCurrentNPC(string npcName)
    {
        currentNpcName = npcName;
        Debug.Log("Hablando con: " + currentNpcName);
    }

    void OnSendButtonClicked()
    {
        string userMessage = inputField.text.Trim();

        if (!string.IsNullOrEmpty(userMessage))
        {
            StartCoroutine(PostRequest(apiUrl, userMessage));
            inputField.text = "";
        }
    }

    IEnumerator PostRequest(string url, string message)
    {
        // Empaquetar datos para la API Flask
        Message msg = new Message { npc = currentNpcName, entrada = message };
        string jsonData = JsonUtility.ToJson(msg);
        byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonData);

        UnityWebRequest request = new UnityWebRequest(url, "POST");
        request.uploadHandler = new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");

        yield return request.SendWebRequest();

        if (request.result != UnityWebRequest.Result.Success)
        {
            chatText.color = Color.red;
            chatText.text += $"Error: {request.error}\n";
            Debug.LogError("Error al enviar mensaje: " + request.error);
        }
        else
        {
            string response = request.downloadHandler.text;
            ChatResponse chatResponse = JsonUtility.FromJson<ChatResponse>(response);
            StartCoroutine(TypeText(chatResponse.response));

            if (currentNpcName == "Guardia" && response.Contains("Has superado el reto")) // Si la respuesta al guardia es correcta pasamos al siguiente nivel
            {
                Debug.Log("Código correcto detectado. Avanzando al siguiente nivel...");
                LevelManager.Instance?.LoadNextLevel();
            }
        }
    }

    IEnumerator TypeText(string fullText)
    {
        chatText.text = "";
        foreach (char c in fullText)
        {
            chatText.text += c;
            yield return new WaitForSeconds(0.01f);  // Velocidad de tipeo
        }
    }
}
