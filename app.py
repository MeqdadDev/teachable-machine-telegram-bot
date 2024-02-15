from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telebot.credentials import BOT_TOKEN, BOT_USERNAME
import cv2 as cv
from teachable_machine_lite import TeachableMachineLite

BOT_USERNAME= "Bla Bla Bot"
# https://telegram.me/BotFather
BOT_TOKEN = "ADD_YOUR_TOKEN_HERE_FROM_BOT_FATHER"

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}, Welcome to {BOT_USERNAME} \n \
                                    Developed by: Meqdad Dev.')

async def cam_stream(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    cap = cv.VideoCapture(0)
    frame_ctr = 0
    image_file_name = "frame.jpg"

    while True:
        ret, frame = cap.read()
        if ret:
            cv.imshow('Cam', frame)
            if frame_ctr > 8:
                cv.imwrite("frame.jpg", frame)
                results = model.classify_frame(image_file_name)
                label = results["label"]
                confidence = results["confidence"]
                print("label:",label)
                print("label:",confidence)
                frame_ctr = 0
                if (label == "ClassA") and (int(confidence) > 95):
                    cv.putText(frame, label , (50,50), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                    cv.imwrite("telegram.jpg", frame)
                    await update.message.reply_text(f'ClassA detected...')
                    await update.message.reply_photo("ClassA.jpg")
                    cv.destroyAllWindows()
                    break
            frame_ctr+=1
        else:
            print("Error: Can't Access Camera")
            
        k = cv.waitKey(1)
        if k% 255 == 27:
            break
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":

    model_path = 'model.tflite'
    labels_path = "labels.txt"

    model = TeachableMachineLite(model_path=model_path, labels_file_path=labels_path)

    app = ApplicationBuilder().token(f"{BOT_TOKEN}").build()

    app.add_handler(CommandHandler("hi", hello))
    app.add_handler(CommandHandler("start", cam_stream))

    app.run_polling()
